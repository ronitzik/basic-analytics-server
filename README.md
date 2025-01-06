# **Basic Analytics Server**

This repository contains the source code for a **FastAPI** based analytics server deployed to **Azure Container Apps**.
The server supports two main functionalities:

1. **`/process_event`**: Accepts and processes events, storing them in an SQLite database.
2. **`/get_reports`**: Fetches reports of events that occurred within a specific timeframe for a given user.

## **Features**

- **FastAPI Framework**: A modern, fast web framework for building APIs with Python.
- **SQLite Database**: A lightweight, serverless database to store events.
- **CI/CD Pipeline**: The repository includes a GitHub Actions pipeline to automatically build and deploy the Docker image to Azure.
- **Dockerized Deployment**: The server is containerized using Docker and deployed to Azure Container Apps for scalability.
