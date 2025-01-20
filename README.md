# FastAPI AI Scraper

![image](https://github.com/user-attachments/assets/d2cacd53-3d03-46ae-9e26-5b543649f009)


**Table of Contents**
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Local Installation](#local-installation)
   - [1. Clone the repository](#1-clone-the-repository)
   - [2. Create a virtual environment](#2-create-a-virtual-environment)
   - [3. Install packages](#3-install-packages)
   - [4. Set up environment variables](#4-set-up-environment-variables)
   - [5. Run the application](#5-run-the-application)
5. [Testing the API with Postman](#testing-the-api-with-postman)
6. [Docker Setup](#docker-setup)
   - [1. Build the Docker image](#1-build-the-docker-image)
   - [2. Run the Docker container](#2-run-the-docker-container)
7. [Usage](#usage)
8. [Deployment Notes](#deployment-notes)

---

## Introduction

This repository provides a **FastAPI** application that scrapes the homepage of a website and uses **Gemini AI** to answer three questions:

1. **Industry**: The industry of the company
2. **Company Size**: The company’s size (small, medium, large, or numeric data)
3. **Location**: The company’s location

All results are exposed via a simple POST endpoint (`/scrape`) secured with a **Bearer token**. In this hobby project, the bearer token is literally **`YOUR_SECRET_KEY`**.

---

## Features
- **FastAPI**: Modern, high-performance Python web framework
- **Pydantic**: Data validation and response modeling
- **Requests + BeautifulSoup**: Light-weight homepage scraping
- **Gemini AI**: Leverages `google-generativeai` to interpret scraped text
- **Bearer Token**: Secured endpoint requiring a valid token
- **Docker**: Easy containerization and deployment

---

## Prerequisites
- **Python** 3.9 or higher  
- **pip** (Python package manager)  
- (Optional) **Docker** if you wish to run the application in a container  

---

## Local Installation

Below is a step-by-step guide to setting up and running the project on your local machine **without Docker**.

### 1. Clone the repository

```bash
git clone https://github.com/aryanbhosale/fastapi-website-scraper.git
cd fastapi-website-scraper
```

### 2. Create a virtual environment

It’s recommended to use a **virtual environment** to keep your dependencies isolated.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install packages

Use the provided `requirements.txt` to install all dependencies:

```bash
pip install -r requirements.txt
```

The key dependencies include:
- **fastapi**  
- **uvicorn** (for local development server)  
- **requests** + **beautifulsoup4** (for scraping)  
- **google-generativeai** (Gemini AI client)  
- **pydantic** (data models)

### 4. Set up environment variables

Create a file called `.env` in the project root (same directory as `requirements.txt`, `Dockerfile`, etc.) with the following contents:

```
SECRET_KEY="YOUR_SECRET_KEY"
GEMINI_API_KEY="your_gemini_api_key"
```

- **SECRET_KEY**: The bearer token used to authenticate incoming requests.  
  - For this project, it’s explicitly set to **`YOUR_SECRET_KEY`**.  
- **GEMINI_API_KEY**: The API key obtained from [Google AI Studio](https://aistudio.google.com/apikey/) or whichever source provided the Gemini credentials.

### 5. Run the application

Launch the FastAPI app locally on port **8000**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- By default, **hot reloading** is not enabled. Add `--reload` if you want the server to restart automatically upon code changes:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

> The server will be accessible at `http://localhost:8000`.

---

## Testing the API with Postman

To confirm everything is working correctly:

1. **Open Postman** or a similar REST client.
2. **Create a new POST request** with the URL:
   ```
   http://localhost:8000/scrape
   ```
3. **Headers**:
   - `Content-Type: application/json`
   - `Authorization: Bearer YOUR_SECRET_KEY`
     *(Using the literal string `YOUR_SECRET_KEY` as the token.)*
4. **Body** (JSON):
   ```json
   {
     "url": "https://www.example.com"
   }
   ```
5. **Send** the request.

You should receive a JSON response like:

```json
{
  "industry": "...",
  "company_size": "...",
  "location": "..."
}
```

If you receive a `401 Unauthorized`, ensure your **Authorization** header is correct (`Bearer YOUR_SECRET_KEY`).

---

## Docker Setup (Using Docker Compose)

### 1. Create a `docker-compose.yaml`

In the root directory (same place as your `Dockerfile` and `requirements.txt`), create a file named **`docker-compose.yaml`** with the following content:

```yaml
services:
  fastapi-scraper:
    container_name: fastapi_scraper
    build: .
    ports:
      - "8000:8000"
    environment:
      SECRET_KEY: ${SECRET_KEY}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
```

- **build: .** tells Docker Compose to use the local `Dockerfile` in the current directory.
- **ports**: `8000:8000` maps container port 8000 → host port 8000.
- **environment**:
  - References environment variables **SECRET_KEY** and **GEMINI_API_KEY** via `${SECRET_KEY}` and `${GEMINI_API_KEY}`.

### 2. (Optional) Create a `.env` file

If you want to store secrets locally without editing the YAML, create a file called **`.env`** in the same directory (this file is automatically recognized by Docker Compose):

```
SECRET_KEY=YOUR_SECRET_KEY
GEMINI_API_KEY=your_gemini_api_key
```

*(Again, we’re literally using `YOUR_SECRET_KEY` as the token for this project.)*

### 3. Build the image

Run:

```bash
docker compose build
```

Docker Compose will:
1. Read your `docker-compose.yaml`.
2. Use your local `Dockerfile` to build the image.
3. Tag it automatically (you’ll see output in the console).

### 4. Run the container

Once built, start the service:

```bash
docker compose up -d
```

- **`-d`** runs it in the background (detached mode).  
- If you omit `-d`, Docker Compose logs will appear directly in your terminal.

### 5. Verify the container is running

```bash
docker compose ps
```

You should see something like:

| NAME               | COMMAND                    | STATE | PORTS                 |
|--------------------|----------------------------|-------|-----------------------|
| fastapi_scraper    | "uvicorn app.main:app …"  | Up    | 0.0.0.0:8000->8000/tcp|

### 6. Check logs (if needed)

```bash
docker compose logs -f fastapi-scraper
```

This follows (streams) the logs of your FastAPI container.

### 7. Test the application

Open Postman or your browser:

- **URL**: `http://localhost:8000/scrape`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer YOUR_SECRET_KEY`
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "url": "https://www.example.com"
  }
  ```

If everything is configured correctly, you’ll receive JSON with keys `industry`, `company_size`, and `location`.  

---

## Usage

### API Endpoint
- **POST** `/scrape`

**Request**:
- **Headers**:
  - `Authorization: Bearer YOUR_SECRET_KEY`
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```

**Response** (example):
```json
{
  "industry": "Software",
  "company_size": "Medium",
  "location": "California, USA"
}
```
