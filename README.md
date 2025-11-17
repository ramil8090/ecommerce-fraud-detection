# E-Commerce Fraud Detection  
A midterm project for the Machine Learning Zoomcamp 2025

## 📁 Repository Structure  
```text
Project-Root/
├── README.md
├── .gitignore
├── data/kaggle.com/umuttuygurr/e-commerce-fraud-detection-dataset/ ← original dataset source
├── docker/predict/ ← Docker setup for prediction service
├── models/ ← saved/trained model artifacts
├── Dockerfile ← container specification
├── notebook.ipynb ← exploratory data analysis + model development notebook
├── train.py ← training script
├── predict.py ← inference/prediction script
├── test.py ← simple testing harness
├── pyproject.toml ← project dependencies & config
└── uv.lock ← locked dependencies
```

## Why This Project Matters
- Fraud detection is a critical challenge in the e-commerce industry: as online transactions rise, so do opportunities for abuse and fraudulent activity.
- Using machine learning allows moving beyond static rule-based systems to adaptively learn from transaction data, detect subtle patterns, and reduce false positives (thus protecting legitimate users while catching fraudsters).
- The full pipeline (data → train → serve) illustrates a practical deployment scenario for fraud detection in real-world settings.

### 📊 Results & Findings
- The exploratory notebook (notebook.ipynb) highlights data distributions, class imbalance, feature importance, and model comparisons.
- Best performing model - Random Forest Classifier achieved [**ROC-AUC = 0.97, precision = 0.94, recall = 0.61**] on the test dataset.
- Feature importance shows that variables such as `shipping_distance_km`, `amount` (purchase amount), `account_age_days`, `avs_match`, `cvv_result` and `three_ds_flag` were strong discriminators of fraud vs non-fraud.

## 🛠 Quick Start / Usage  
### Prerequisites  
- Python 3.x  
- Install uv - an extremely fast Python package and project manager, written in Rust. (`pip install uv`)
- Install project dependencies via uv (`uv sync --locked`)  
- Docker (optional, for containerised inference)

### Training the Model 
```bash
python train.py
```

### Running Prediction API service
```bash
python predict.py
```

### Running Tests
```bash
python test.py
```

## Using Docker
```bash
docker build -t ecommerce-fraud-prediction .
docker run -it --rm -p 9696:9696 ecommerce-fraud-prediction:latest
```
Then send requests (e.g., via Postman or Curl) to the service to get fraud predictions. See examples below:
```bash
curl --location 'http://127.0.0.1:9696/predict' \
--header 'Content-Type: application/json' \
--data '{
    "account_age_days":141,
    "total_transactions_user":47,
    "avg_amount_user":147.93,
    "amount":84.75,
    "country":"FR",
    "bin_country":"FR",
    "channel":"web",
    "merchant_category":"travel",
    "promo_used":0,
    "avs_match":1,
    "cvv_result":1,
    "three_ds_flag":1,
    "shipping_distance_km":370.95,
    "day":5,
    "month":1,
    "hour":4,
    "night_hours":1
}'
```

```bash
curl --location 'http://127.0.0.1:9696/predict' \
--header 'Content-Type: application/json' \
--data '{
    "account_age_days":30,
    "total_transactions_user":47,
    "avg_amount_user":147.93,
    "amount":84.75,
    "country":"FR",
    "bin_country":"US",
    "channel":"web",
    "merchant_category":"travel",
    "promo_used":1,
    "avs_match":0,
    "cvv_result":0,
    "three_ds_flag":0,
    "shipping_distance_km":1000.95,
    "day":5,
    "month":1,
    "hour":4,
    "night_hours":1
}'
```

## Acknowledgements & References
- Dataset from Kaggle: “E-commerce Fraud Detection” by umuttuygurr (https://www.kaggle.com/datasets/umuttuygurr/e-commerce-fraud-detection-dataset/data).
- Inspired by various fraud detection research and industrial practices.
- Built as part of the Machine Learning Zoomcamp 2025 midterm assignment.
