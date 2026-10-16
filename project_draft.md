# Project Draft: Discarded Material Identification System

## 1. Project Overview
This project is an end-to-end Machine Learning solution designed to detect and classify waste objects in images. It leverages the state-of-the-art **YOLOv5** object detection model to achieve high accuracy and real-time performance. The system is built with a production-ready mindset, featuring a modular architecture, automated pipelines, and CI/CD integration for cloud deployment (AWS/Azure).

## 2. Key Features
- **Object Detection**: Utilizes YOLOv5 for detecting various classes of waste (e.g., biodegradable, non-biodegradable, or specific material types).
- **End-to-End Pipeline**: Includes distinct stages for data ingestion, validation, model training, and evaluation.
- **Web Interface**: A Flask-based web application (`app.py`) allows users to upload images and visualize detection results.
- **Modular Codebase**: Organized into components, pipelines, entities, and constants for maintainability and scalability.
- **CI/CD Deployment**: Automated deployment workflows using GitHub Actions to build Docker images and deploy to AWS EC2 (via ECR) or Azure Web Apps (via ACR).

## 3. Technology Stack
- **Language**: Python 3.7+
- **Deep Learning Framework**: PyTorch (via YOLOv5)
- **Web Framework**: Flask
- **Containerization**: Docker
- **Cloud Providers**: AWS (ECR, EC2)
- **CI/CD**: GitHub Actions
- **Utilities**: `dill` (serialization), `from-root` (path management)

## 4. Project Structure
The project follows a structured modular layout:

- **`wasteDetection/`**: The core package containing the backend logic.
    - **`components/`**: Implements individual pipeline steps.
        - `data_ingestion.py`: Handles data downloading and extraction.
        - `data_validation.py`: Validates data format and integrity.
        - `model_trainer.py`: Manages the YOLOv5 training process.
    - **`pipeline/`**: Orchestrates the components.
        - `training_pipeline.py`: Defines the sequence of execution for training.
    - **`entity/`**: Defines data classes and configuration objects.
    - **`constant/`**: Stores hardcoded constants and configuration paths.
    - **`utils/`**: Helper functions for common tasks (e.g., file I/O, encoding).
    - **`exception/`** & **`logger/`**: Custom error handling and logging mechanisms.

- **`templates/`**: HTML templates for the Flask web application.
- **`app.py`**: The entry point for the Flask web server.
- **`requirements.txt`**: List of project dependencies.
- **`setup.py`**: Configuration for packaging the project as a library.
- **`Dockerfile`**: Instructions for building the container image.
- **`.github/workflows/`**: YAML configuration files for GitHub Actions CI/CD pipelines.

## 5. Workflows
1.  **Data Ingestion**: Download dataset from source (e.g., GDrive, S3) and unzip.
2.  **Data Validation**: Ensure dataset structure matches YOLOv5 requirements.
3.  **Model Training**: Fine-tune the YOLOv5 model on the validated dataset.
4.  **Inference**: The web app uses the trained model to predict bounding boxes on new images.

## 6. Deployment Strategy
The project currently supports two primary deployment targets:

### AWS Deployment
1.  **Containerize**: Build a Docker image of the application.
2.  **Registry**: Push the image to AWS Elastic Container Registry (ECR).
3.  **Compute**: Pull and run the image on an AWS EC2 instance.
4.  **Automation**: GitHub Actions handles the build-and-push process upon code changes.

