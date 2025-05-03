# Article Recommender System

This project implements an article recommendation system that suggests related content to users based on what they are currently reading.

## Getting Started (Quick Start)

### Using Pre-built Applications (Recommended)

1. Download and install the application for your platform:
   - Windows: from `interface/releases/Windows`
   - MacOS: from `interface/releases/MacOS`
   - Linux: from `interface/releases/Linux`

2. Launch the application
   
   **IMPORTANT NOTE:** The first connection to the server may take up to 1-2 minutes **IF** the server was scaled down to zero.

3. Start searching for articles!

## Project Overview

This system consists of two main components:

1. Backend service - Semantic search and recommender system, written primarily in Python (hosted at https://article-recommender-system.fly.dev)
2. Frontend interface - Desktop application for article browsing, written in Rust(Tauri) and Svelte

## Development Setup

### Prerequisites

- For frontend development: 
  - Rust, Node.js, and Tauri (follow guide at: https://tauri.app/start/prerequisites/)

- For backend development only:
  - Python 3.8+ with pip
  - Python dependencies: `pip install -r system/requirements.txt`

### Running in Development Mode

#### Backend (if you need to run a local server)

1. Start the backend service:

   ```bash
   python system/main.py
   ```

   This starts the service on port 50051.

2. Update the server URL in the frontend to use the local server.

#### Frontend

1. Navigate to the interface directory:
   ```bash
   cd interface/ArticleApp/
   ```
2. Run in development mode:
   ```bash
   npm run tauri dev
   ```

## Project Structure

- `system/`: Recommender system and database
- `interface/`: Frontend application code
- `proto/`: Protocol buffer definitions for backend-frontend communication

## Key Components

### Python Modules

- **prepare_dataset.py**  
  Prepares the article dataset by generating embeddings and building a search index.

  ```bash
  python system/prepare_dataset.py  # Run this if you need to rebuild the search index
  ```

- **search.py**  
  Core search functionality that uses sentence embeddings and vector search to find relevant articles.

- **main.py**  
  Runs the system as a gRPC service that the interface connects to.
