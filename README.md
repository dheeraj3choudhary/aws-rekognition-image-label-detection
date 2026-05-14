# aws-rekognition-image-label-detection

Detect and label objects in images using Amazon Rekognition, FastAPI, and Streamlit.

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI/ML**: Amazon Rekognition (`detect_labels`)
- **Language**: Python 3.11

---

## Project Structure

```
aws-rekognition-image-label-detection/
├── backend/
│   ├── main.py
│   ├── rekognition.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- AWS Account with an IAM user having `AmazonRekognitionReadOnlyAccess` policy

---

## AWS Setup

1. Go to **IAM → Users → Create User**
2. Attach policy: `AmazonRekognitionReadOnlyAccess`
3. Generate **Access Key + Secret Key**
4. Copy `.env.example` to `.env` and fill in your credentials

```bash
cp .env.example .env
```

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

---

## Running Locally (Without Docker)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at: `http://localhost:8501`

---

## Running with Docker

```bash
docker-compose up --build
```

| Service  | URL                   |
|----------|-----------------------|
| Frontend | http://localhost:8501 |
| Backend  | http://localhost:8000 |

---

## API Endpoints

| Method | Endpoint  | Description                        |
|--------|-----------|------------------------------------|
| GET    | /health   | Health check                       |
| POST   | /detect   | Upload image and get detected labels|

### Example Response

```json
{
  "filename": "dog.jpg",
  "labels": [
    {
      "name": "Dog",
      "confidence": 99.23,
      "categories": ["Animal", "Pet"]
    },
    {
      "name": "Outdoor",
      "confidence": 87.45,
      "categories": ["Nature"]
    }
  ]
}
```

---

## How It Works

1. User uploads an image via the Streamlit UI
2. Streamlit sends the image to the FastAPI `/detect` endpoint
3. FastAPI forwards the image bytes to Amazon Rekognition
4. Rekognition returns labels with confidence scores and categories
5. Results are displayed in the Streamlit UI with confidence progress bars

---

## Supported Image Formats

- JPEG
- PNG
- WEBP