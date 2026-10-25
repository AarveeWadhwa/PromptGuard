# PromptGuard

**PromptGuard: An Explainable NLP-Based Detector for Prompt Injection and Jailbreak Attacks**

PromptGuard is a full-stack NLP security application designed to classify text as benign or potentially associated with prompt injection/jailbreak attacks and provide human-readable linguistic explanations.

## Planned models
- Logistic Regression — TF-IDF baseline
- Random Forest — classical ML baseline
- DistilBERT — fine-tuned transformer model

## Planned datasets
### Injection / jailbreak
- deepset/prompt-injections
- hackaprompt/hackaprompt-dataset (subsample)
- rubend18/ChatGPT-Jailbreak-Prompts

### Benign
- tatsu-lab/alpaca (subsample)
- OpenAssistant/oasst1 (subsample)

## Current application
The FastAPI backend currently includes an explainability marker layer so the frontend can be developed before model training is complete. The fallback is explicitly identified in API responses and will later be replaced by the trained model pipeline.

## Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Docker
```bash
docker compose up --build
```

Frontend: http://localhost:3000
Backend: http://localhost:8000
