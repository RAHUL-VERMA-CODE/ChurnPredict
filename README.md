# Customer Churn Prediction

An ANN-based model that predicts whether a bank customer is likely to churn, served through a FastAPI backend with a Streamlit frontend.

## Live Demo

- **API (Render):** https://churnpredict-1.onrender.com
- **API health check:** https://churnpredict-1.onrender.com/health
- **API docs (Swagger):** https://churnpredict-1.onrender.com/docs

> Note: the backend is on Render's free tier, so it sleeps when idle. The first request after inactivity can take 30–50 seconds to wake up.

## Project Structure

```
ANN_Project/
├── app.py                     # Streamlit UI (calls the FastAPI backend)
├── main.py                    # FastAPI app — /, /health, /predict
├── requirements.txt
├── model/
│   ├── predict_output.py      # loads model.h5 + encoders/scaler, runs prediction
│   ├── model.h5
│   ├── label_encoder_gender.pkl
│   ├── Onehot_encoder_geo.pkl
│   └── scaler.pkl
├── schema/
│   └── user_input.py          # pydantic request schema for /predict
├── experiments.ipynb          # model training/experimentation
├── gridsearch.ipynb           # hyperparameter tuning (layers/neurons)
└── Churn_Modelling.csv        # training data
```

## How It Works

1. **Training** (`experiments.ipynb`, `gridsearch.ipynb`) — the raw data is cleaned, `Gender` is label-encoded, `Geography` is one-hot encoded, features are scaled, and a Keras ANN is trained to predict the `Exited` column. The trained model and preprocessing objects (`scaler`, encoders) are saved as `.h5`/`.pkl` files.
2. **Backend** (`main.py` + `model/predict_output.py`) — FastAPI loads the saved model and preprocessors once at startup. The `/predict` endpoint validates incoming data against `schema/user_input.py`, applies the same preprocessing used in training, and returns a churn probability.
3. **Frontend** (`app.py`) — a Streamlit form collects customer details and sends them to the FastAPI `/predict` endpoint, then displays the churn probability and verdict.

## Setup

```bash
# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# install dependencies
pip install -r requirements.txt
```

## Running Locally

Start the backend and frontend in **two separate terminals**:

```bash
# terminal 1 — FastAPI backend
uvicorn main:app --reload

# terminal 2 — Streamlit frontend
streamlit run app.py
```

By default `app.py` points at the deployed Render API. To point it at your local backend instead, set an environment variable before running Streamlit:

```bash
# Windows (PowerShell)
$env:API_URL="http://127.0.0.1:8000"; streamlit run app.py

# macOS/Linux
API_URL="http://127.0.0.1:8000" streamlit run app.py
```

Or create `.streamlit/secrets.toml` with:
```toml
API_URL = "http://127.0.0.1:8000"
```

## API Endpoints

| Method | Endpoint    | Description                          |
|--------|-------------|---------------------------------------|
| GET    | `/`         | Health message                        |
| GET    | `/health`   | Status + model version                |
| POST   | `/predict`  | Takes customer data, returns churn probability |

### Example `/predict` request body

```json
{
  "CreditScore": 650,
  "Geography": "France",
  "Gender": "Male",
  "Age": 35,
  "Tenure": 3,
  "Balance": 50000,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 60000
}
```

## Deployment

- **Backend** is deployed on [Render](https://render.com) as a web service (loads TensorFlow + the saved `.h5` model).
- **Frontend** is meant to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud) — set `API_URL` under the app's Secrets to your backend's public URL.

## Tech Stack

- TensorFlow / Keras — ANN model
- scikit-learn — preprocessing (encoders, scaler)
- FastAPI + Pydantic — backend API and request validation
- Streamlit — frontend UI
- Render — backend hosting
