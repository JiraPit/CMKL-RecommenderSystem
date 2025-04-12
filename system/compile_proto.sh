#!/bin/bash

# Set the base directory to the project root
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO_FILE="$BASE_DIR/proto/system_backend.proto"
OUTPUT_DIR="$BASE_DIR/system"

# Check if the proto file exists
if [ ! -f "$PROTO_FILE" ]; then
  echo "Error: Proto file $PROTO_FILE not found!"
  exit 1
fi

# Create proto directory inside system if it doesn't exist
mkdir -p "$OUTPUT_DIR/proto"

# Generate the Python code from proto definitions
python3 -m grpc_tools.protoc \
  --proto_path="$BASE_DIR" \
  --python_out="$OUTPUT_DIR" \
  --grpc_python_out="$OUTPUT_DIR" \
  "$PROTO_FILE"

# Check if the generation was successful
if [ $? -eq 0 ]; then
  echo "Successfully generated gRPC code!"
  echo "Generated files:"
  echo "  - $OUTPUT_DIR/proto/system_backend_pb2.py"
  echo "  - $OUTPUT_DIR/proto/system_backend_pb2_grpc.py"

  # Make the Python import path work properly
  # Create an __init__.py file in the proto directory if it doesn't exist
  touch "$OUTPUT_DIR/proto/__init__.py"

  echo "Created $OUTPUT_DIR/proto/__init__.py for proper imports"
else
  echo "Error generating gRPC code"
  exit 1
fi

echo "Done!"

