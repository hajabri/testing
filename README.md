# ML Service

![Coveo Logo](docs/graphics/coveo-logo.png "Coveo Logo")

> PROPRIETARY and CONFIDENTIAL, Coveo Solutions Inc.
> v2.0.0 - Last Edited 2024-10-01.

**A Python project that serves an NLP model to solve a multiple choice question answering (MCQA) problem as a REST API.**
**The model fills in a missing word ([BLANK]) in a passage of text, given for possible choice.**

## Table of Contents
1. Overview

2. Folder Structure

3. Setup & Installation

4. Running the service locally

5. Docker Build & Run

6. Testing the MCQA Endpoint

7. Known Limitations/Future Work

## Overview

Documentation on getting started.

### Prerequisites

- Python 3.10
- Poetry
- Makefile (GNU Make)

### Commands

Commands are provided in this project's Makefile:

- `make install` Install project dependencies (via Poetry).
- `make lock` Update the Poetry lock file.
- `make test` Run the test suite.
- `make notebooks` Run a Jupyter environment.
- `make docker-build`: Build a docker image. TODO: This is currently not a complete dockerfile.

### Structure

```text
artifacts/           Skeleton structure for artifacts
    datasets/
    models/
docker/              Dockerfile
docs/                Documentation and graphics
ml_service/          Python source code
notebooks/           Jupyter notebooks
tests/               Python test suite
Makefile             Runnable commands
pyproject.toml       Configuration for project tools
README.md            This read me
```

### Run the service

Set up:

```bash
make install
make pull-spacy-corpora
```

Start the service:

```bash
export DEVELOPMENT_MODE=true
poetry run python ml_service/main.py
```

Use the service:

- Visit the index (e.g., via a browser) at: `http://127.0.0.1:8080`
- Visit the docs at: `http://127.0.0.1:8080/docs`
- Send a request: `http://127.0.0.1:8080/chunkify?text=Hello%20word.%20Nice%20to%20meet%20again.`
