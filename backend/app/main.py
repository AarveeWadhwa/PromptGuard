from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictionRequest, PredictionResponse
from .predictor import predict

app = FastAPI(title="PromptGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "PromptGuard API"}

@app.get("/model-info")
def model_info():
    return {
        "primary_model": "DistilBERT (fine-tuned)",
        "baseline_models": ["Logistic Regression", "Random Forest"],
        "classes": ["benign", "prompt_injection"]
    }

@app.post("/predict", response_model=PredictionResponse)
def prediction(request: PredictionRequest):
    return predict(request.text)
