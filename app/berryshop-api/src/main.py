import os
from datetime import datetime, timezone

from fastapi import FastAPI

# The starter app keeps its data in memory on purpose.
# This makes the first version easy to read before adding databases or queues.
PRODUCTS = [
    {
        "id": 1,
        "name": "Smurfberry Jam",
        "price": 5.99,
        "currency": "USD",
    },
    {
        "id": 2,
        "name": "Forest Berry Pie",
        "price": 8.49,
        "currency": "USD",
    },
    {
        "id": 3,
        "name": "Blue Moon Smoothie",
        "price": 4.75,
        "currency": "USD",
    },
]

app = FastAPI(
    title="BerryShop API",
    version="0.1.0",
    description="A tiny API used to teach Kubernetes and DevSecOps basics.",
)


def get_runtime_settings() -> dict[str, str]:
    """Read environment-based settings in one place for easy teaching."""
    return {
        "app_env": os.getenv("APP_ENV", "local"),
        "cluster_name": os.getenv("CLUSTER_NAME", "local-dev"),
        "welcome_banner": os.getenv(
            "WELCOME_BANNER",
            "Welcome to BerryShop API from SmurfSecOps Lab",
        ),
        "log_level": os.getenv("LOG_LEVEL", "info"),
    }


@app.get("/")
def read_root() -> dict[str, str]:
    settings = get_runtime_settings()
    return {
        "service": "berryshop-api",
        "message": settings["welcome_banner"],
        "environment": settings["app_env"],
        "cluster": settings["cluster_name"],
        "docs": "/docs",
    }


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "berryshop-api",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/products")
def list_products() -> dict[str, object]:
    return {
        "count": len(PRODUCTS),
        "items": PRODUCTS,
    }


@app.get("/api/v1/info")
def read_info() -> dict[str, str]:
    return get_runtime_settings()
