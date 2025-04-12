import sqlite3
import grpc
from concurrent import futures
import time
from pathlib import Path
from search import search
import proto.system_backend_pb2_grpc as pb_grpc
import proto.system_backend_pb2 as pb

# Set the path to the article database
ARTICLE_DB_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "article.db"
).resolve()


class RecommenderServicer(pb_grpc.RecommenderServiceServicer):
    """Implementation of the RecommenderService service."""

    def Search(self, request, context):
        """Implements the Search RPC method."""
        print("Received search request:", request.search_term)
        try:

            # Call the search function
            article_ids = search(request.search_term, request.num_results)

            # Create and populate the response
            response = pb.SearchResponse(article_ids=article_ids)
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error performing search: {str(e)}")
            return pb.SearchResponse()

    def GetArticleInfo(self, request, context):
        """Implements the GetArticleInfo RPC method."""
        print("Received GetArticleInfo request for article ID:", request.article_id)
        try:
            # Connect to the SQLite database
            with sqlite3.connect(ARTICLE_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Query for article info
                cursor.execute(
                    "SELECT article_id, doc_full_name, doc_description FROM article WHERE article_id = ?",
                    (request.article_id,),
                )

                # Fetch the result
                result = cursor.fetchone()

                if result:
                    # Create and populate the response
                    response = pb.GetArticleInfoResponse(
                        name=result["doc_full_name"],
                        description=result["doc_description"],
                    )
                    return response
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(
                        f"Article with ID {request.article_id} not found"
                    )
                    return pb.GetArticleInfoResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error retrieving article info: {str(e)}")
            return pb.GetArticleInfoResponse()

    def GetArticleFull(self, request, context):
        """Implements the GetArticleFull RPC method."""
        print("Received GetArticleFull request for article ID:", request.article_id)
        try:
            # Connect to the SQLite database
            with sqlite3.connect(ARTICLE_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Query for full article
                cursor.execute(
                    "SELECT article_id, doc_full_name, doc_description, doc_body FROM article WHERE article_id = ?",
                    (request.article_id,),
                )

                # Fetch the result
                result = cursor.fetchone()

                if result:
                    # Create and populate the response
                    response = pb.GetArticleFullResponse(
                        name=result["doc_full_name"],
                        description=result["doc_description"],
                        body=result["doc_body"],
                    )
                    return response
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(
                        f"Article with ID {request.article_id} not found"
                    )
                    return pb.GetArticleFullResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error retrieving full article: {str(e)}")
            return pb.GetArticleFullResponse()


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add the servicer to the server
    pb_grpc.add_RecommenderServiceServicer_to_server(RecommenderServicer(), server)

    # Listen on port 50051
    server.add_insecure_port("0.0.0.0:6789")
    server.start()

    print("System backend started on port 6789...")

    try:
        # Keep thread alive
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
