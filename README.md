# CMKL Recommender System

A semantic search-based article recommender system for discovering relevant articles based on user queries and activities.

## Project Overview

This system consists of two main components:

1. Backend service - Semantic search and recommender system, written primarily in Python
2. Frontend interface - Desktop application for article browsing, written in Rust(Tauri) and Svelte

## Project Structure

- `system/`: Backend code and utilities
- `interface/`: Frontend application code
- `releases/`: Pre-built application binaries
- `proto/`: Protocol buffer definitions for backend-frontend communication

## Setup and Running

### Prerequisites

- Python 3.8+ with pip
- Python dependencies, installed with `pip install -r system/requirements.txt`
- For development only, Rust and Node.js. 

### Running the System

1. Start the backend service:

   ```bash
   python system/run_as_backend.py
   ```

   This starts the service on port 6789.

2. Launch the interface application:
   - Windows: Run `releases/windows/ArticleApp.exe`
   - macOS: Run `releases/macos/ArticleApp.app`
   - Linux: Run `releases/linux/ArticleApp.AppImage`

### Standalone Demo

For a simple command-line demo of the search functionality:

```bash
python system/stand_alone_demo/demo_search.py
```

## Key Components

### Python Modules

- **prepare_dataset.py**  
  Prepares the article dataset by generating embeddings and building a search index.

  ```bash
  python system/prepare_dataset.py  # Run this if you need to rebuild the search index
  ```

- **search.py**  
  Core search functionality that uses sentence embeddings and vector search to find relevant articles.

- **run_as_backend.py**  
  Runs the system as a gRPC service that the interface connects to.

- **stand_alone_demo/demo_search.py**  
  Simple CLI demo for testing the search functionality directly.

