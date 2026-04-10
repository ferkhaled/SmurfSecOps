# BerryShop API

BerryShop API is the first application in SmurfSecOps Lab.
It is intentionally small so learners can understand the full stack quickly.

## Features

- root welcome endpoint
- health endpoint
- tiny berry catalog endpoint
- runtime info endpoint that shows environment-driven configuration

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Test locally

```powershell
pytest
```

## Build container image

```powershell
docker build -t berryshop-api:0.1.0 .
docker save berryshop-api:0.1.0 -o berryshop-api.tar
```

## API endpoints

- `GET /`
- `GET /healthz`
- `GET /api/v1/products`
- `GET /api/v1/info`
