# Training pipeline

This directory will contain the reproducible dataset preparation and training scripts.

Planned pipeline:
1. Download/subsample injection datasets: deepset/prompt-injections, hackaprompt/hackaprompt-dataset, rubend18/ChatGPT-Jailbreak-Prompts.
2. Download/subsample benign datasets: tatsu-lab/alpaca, OpenAssistant/oasst1.
3. Normalize to `text,label`.
4. Deduplicate and create stratified train/validation/test splits.
5. Train TF-IDF + Logistic Regression and Random Forest baselines.
6. Fine-tune DistilBERT.
7. Save artifacts into `backend/models/`.
