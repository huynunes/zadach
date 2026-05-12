import os
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("HF_MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
device = 0 if os.getenv("USE_GPU", "false").lower() == "true" else -1

try:
    logger.info(f"Loading Hugging Face model: {MODEL_NAME}")
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME, device=device)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load Hugging Face model: {e}")
    classifier = None

def analyze_text(text: str):
    if classifier is None:
        raise RuntimeError("ML model is not initialized. Check logs.")
    try:
        result = classifier(text)[0]
        return result["label"], result["score"]
    except Exception as e:
        logger.error(f"Error during model inference: {e}")
        raise