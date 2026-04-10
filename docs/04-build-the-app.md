# 04 - Build The App

The first app in the lab is `BerryShop API`.
It is intentionally small so learners can inspect the whole codebase quickly.

## What the API does today

- returns a root welcome response
- exposes a health endpoint
- returns a small catalog of berry products
- exposes simple runtime info from environment variables

## Run the app locally

```powershell
cd app/berryshop-api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/healthz`
- `http://127.0.0.1:8000/docs`

## Run the tests

```powershell
pytest
```

## Learning goal

At this stage, focus on understanding the app and the test flow before moving into containers and Kubernetes.
