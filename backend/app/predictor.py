
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from .explainability import find_markers


# backend/models/distilbert_promptguard/
MODEL_DIR = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "distilbert_promptguard"
)

MODEL_NAME = "DistilBERT fine-tuned"
MAX_LENGTH = 256

_tokenizer = None
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model():
    """Load the trained model once and reuse it for predictions."""
    global _tokenizer, _model

    if _model is not None and _tokenizer is not None:
        return _tokenizer, _model

    if not (MODEL_DIR / "config.json").is_file():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_DIR}. "
            "Place your extracted distilbert_promptguard folder "
            "inside backend/models/."
        )

    _tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_DIR),
        local_files_only=True,
    )
    _model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_DIR),
        local_files_only=True,
    )
    _model.to(_device)
    _model.eval()

    return _tokenizer, _model


def predict(text: str):
    """Classify a prompt with trained DistilBERT and explain markers."""
    if not text or not text.strip():
        raise ValueError("Prompt text cannot be empty.")

    tokenizer, model = load_model()

    inputs = tokenizer(
    text,
    return_tensors="pt",
    truncation=True,
    max_length=MAX_LENGTH,
    padding=True,
)

# DistilBERT does not accept token_type_ids.
    inputs.pop("token_type_ids", None)

    inputs = {
        key: value.to(_device)
        for key, value in inputs.items()
    }

    with torch.inference_mode():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)[0]
        predicted_id = int(torch.argmax(probabilities).item())
        confidence = float(probabilities[predicted_id].item())

    # Prefer the class names saved in the trained model configuration.
    id2label = model.config.id2label
    raw_label = str(
        id2label.get(predicted_id, id2label.get(str(predicted_id), ""))
    ).strip().lower()

    # Normalize common label naming conventions.
    if raw_label in {
        "benign", "safe", "normal", "0", "label_0"
    }:
        label = "benign"
    elif raw_label in {
        "prompt_injection", "prompt injection",
        "jailbreak", "malicious", "1", "label_1"
    }:
        label = "prompt_injection"
    else:
        raise ValueError(
            f"Unrecognized model class {raw_label!r}. "
            f"Check model.config.id2label: {id2label}"
        )

    markers = find_markers(text)

    if label == "prompt_injection":
        explanation = (
            "Fine-tuned DistilBERT classified this prompt as "
            "potential prompt injection or jailbreak."
        )
        if markers:
            explanation += (
                " The marker detector also identified linguistic "
                "indicators listed below."
            )
        else:
            explanation += (
                " The marker detector did not identify any of its "
                "configured patterns; the classification is based "
                "on the model prediction."
            )
    else:
        explanation = (
            "Fine-tuned DistilBERT classified this prompt as benign. "
            "This does not guarantee that the prompt is safe."
        )
        if markers:
            explanation += (
                " Note: the independent marker detector found "
                "suspicious patterns, so review this result carefully."
            )

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "markers": markers,
        "explanation": explanation,
        "model": MODEL_NAME,
    }
