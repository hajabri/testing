# MCQA Model Service

![Coveo Logo](docs/graphics/coveo-logo.png "Coveo Logo")

> PROPRIETARY and CONFIDENTIAL, Coveo Solutions Inc.  
> **v1.0.0 - Last Edited 2024-10-01**  
>  
> For the full challenge description, see [INSTRUCTIONS.md](INSTRUCTIONS.md).

A Python project that serves a **Multiple Choice Question Answering (MCQA)** model as a REST API.  
The model fills in a missing word (`[BLANK]`) in a passage of text, given four possible choices.

---

## Table of Contents

1. [Overview](#overview)  
2. [Folder Structure](#folder-structure)  
3. [Setup & Installation](#setup--installation)  
4. [Configuration & GPU Toggle](#configuration--gpu-toggle)  
5. [Running the Service Locally](#running-the-service-locally)  
6. [Docker Build & Run](#docker-build--run)  
7. [Testing the MCQA Endpoint](#testing-the-mcqa-endpoint)  
8. [Automation via Makefile](#automation-via-makefile)  
9. [Known Limitations / Future Work](#known-limitations--future-work)

---

## Overview

This project:

- **Loads** a pretrained Hugging Face MCQA model (in `artifacts/models/`)  
- **Serves** it via FastAPI, providing an endpoint to fill `[BLANK]` from four choices  
- **Containerizes** the service with Docker for easy deployment  
- **Enables** optional GPU usage if needed (by toggling settings in `config.yaml` and building an NVIDIA-based Docker image)

Below is a simple **data flow diagram** illustrating how a user sends text with `[BLANK]` to your FastAPI service, which loads the HuggingFace MCQA model to compute the best choice. The response is then returned to the user with a chosen label and confidence score.

```mermaid
flowchart LR
    U[User] -->|POST /mcqa| A[FastAPI / MCQA Endpoint]
    A -->|Load config & Model Path<br>(config.yaml)| C[MCQA Model Code]
    C -->|Inference using HF Model| D[Model Artifacts<br>(artifacts/models)]
    C -->|Return best choice & confidence| A
    A -->|JSON response| U

> **Note**: We do **not** train the model here. We only serve it for inference.

---

## Folder Structure

```plaintext
.
├── artifacts/
│   ├── datasets/       # (train.csv, test.csv, if needed for local checks)
│   └── models/         # Model files: config.json, model.safetensors, etc.
├── config.yaml         # Main user-editable config (model path, gpu_enabled, etc.)
├── docker/
│   └── Dockerfile      # Docker build script
├── docs/
│   └── graphics/       # Assets (e.g., coveo-logo.png)
├── ml_service/
│   ├── endpoints.py    # Defines /mcqa endpoint
│   ├── main.py         # FastAPI app entry point
│   ├── mcqa_model.py   # Model loading & inference
│   ├── settings.py     # Loads config.yaml, provides typed settings
├── notebooks/
│   └── Train_MCQA_Model.ipynb  # Provided by scientists (optional reference)
├── tests/
│   ├── unit/
│   │   └── ml_service/
│   │       └── test_endpoints.py  # Basic test example
│   └── load_test.py               # Simple concurrency/throughput test
├── Makefile            # Commands for dev env setup, linting, testing, docker
├── pyproject.toml      # Poetry config for dependencies
├── poetry.lock         # Locked dependency versions
├── README.md           # This file
├── ANALYSIS.md         # Operational analysis
└── DESIGN.md           # Design & future improvements
```

## Setup & Installation
### Prerequisites 
- Python 3.10
- Poetry (For dependency management) 
- Docker (For Container builds)
- GNU Make (optional, but convenient for running commands)

### Local Python Environment
```# install dependencies```
```poetry install```

## Configuration & GPU Toggle
All main settings reside in config.yaml, for example:

yaml
Copy code
model:
  path: "artifacts/models"
  gpu_enabled: false

service:
  host: "0.0.0.0"
  port: 8080
  development_mode: false


- ```model.path```: Points to your MCQA model files.
- ```model.gpu_enabled```: Set to true and build a GPU Docker image if you want CUDA-based inference.
- service.host / service.port: Where the FastAPI app listens.
**Data scientists can modify config.yaml without touching Python code.**

## Running the Service Locally 
```# Activate Poetry shell if you wish```
```poetry shell```

```# Run the FastAPI service```
```poetry run python -m ml_service.main```

- Open http://127.0.0.1:8080/docs to see and try out the /mcqa endpoint interactively.


## Docker Build & Run 
### CPU-Only Docker
1. Build:
```docker build -t ml_nlp_service:latest -f docker/Dockerfile .```

2. Run:
```docker run -p 8080:8080 ml_nlp_service:latest```

3. Test at ```http://localhost:8080/docs.```

### GPU Docker (Optional)
- Use an NVIDIA base image in the Dockerfile or add ```-debug-arg``` to switch  images. 
- Set ```gpu_enabled:true``` in the config.yaml
- **Run** with :
```docker run --gpus all -p 8080:8080 ml_nlp_service:latest```
-Ensure you have the NVIDIA Container Toolkit installed on your host. 

### Testing the MCQA Endpoint 
**Endpoint**: ```/mcqa```
**Method**: ```POST```
**Request Body**(JSON):
{
  "text": "It was a [BLANK] day.",
  "choice1": "bright",
  "choice2": "green",
  "choice3": "dark",
  "choice4": "heavy"
}
**Example cURL**:
```curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text":"It was a [BLANK] day.","choice1":"bright","choice2":"green","choice3":"dark","choice4":"heavy"}' \
  http://127.0.0.1:8080/mcqa
```

**Response(example)**:
```
{
  "chosen_label": "bright",
  "confidence": 0.88 
  }
  ```
## Automation via Makefile
We provide a Makefile with common commands:

- ```make install```: Install Python dependencies via Poetry.
- ```make format```: Auto-format code (using black + isort).
- ```make lint```: Check code style (flake8).
- ```make test```: Run unit tests with pytest.
- ```make load-test```: Run a mini concurrency test (tests/- load_test.py) against a running service.
- ```make docker-build```: Build the Docker image.
- ```make docker-run```: Run the Docker container on port 8080.

### Example usage:
```
bash
Copy code
make install     # Installs dependencies
make format      # Formats code
make lint        # Lints code
make test        # Runs unit tests
make load-test   # Minimal load test
make docker-build
make docker-run
```

## Known Limitations/Future Work
1. **Batch Inference**: Currently processes requests one at a time. Batching could improve throughput.
2. **Model Registry**: A future step could be storing multiple model versions in S3 or MLflow, referencing them dynamically.
3. **Monitoring & Logging**: Adding Prometheus metrics or centralized logging would help in production.
4. **CI/CD**: A pipeline to automatically build/test Docker on each commit would reduce deployment friction.
5. **Quantization / TorchScript**: For faster CPU inference, consider model optimizations.

**Happy MCQA-ing!**s