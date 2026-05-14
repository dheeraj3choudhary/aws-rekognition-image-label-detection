import boto3
import os
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def validate_and_convert_image(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def detect_labels(image_bytes: bytes, max_labels: int = 20, min_confidence: float = 70.0):
    image_bytes = validate_and_convert_image(image_bytes)

    response = client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    labels = []
    for label in response.get("Labels", []):
        labels.append({
            "name": label["Name"],
            "confidence": round(label["Confidence"], 2),
            "categories": [c["Name"] for c in label.get("Categories", [])],
        })

    return labels