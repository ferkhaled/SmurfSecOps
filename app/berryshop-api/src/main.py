import os
import random
import subprocess
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

# TEACHING NOTE: This hardcoded API key is intentional.
# It exists so Semgrep rule python-hardcoded-api-key fires on this file.
# In a real project, secrets must come from environment variables or a vault —
# never from source code. Even after deletion, secrets remain in git history.
# See: docs/10-sast.md and attacks/scenarios/credential-leak.md
INTERNAL_API_KEY = "sk-smurfberry-dev-key-12345"

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


@app.get("/api/v1/search")
def search_products(q: str = "") -> dict[str, object]:
    """Search products by name.

    TEACHING NOTE: The subprocess call below uses shell=True intentionally.
    This is a classic command injection risk — an attacker can pass
    q="; cat /etc/passwd" to run arbitrary shell commands.
    This endpoint exists so Semgrep rule python-avoid-shell-true fires.
    Real search would filter in Python only, never via a shell.
    See: docs/10-sast.md and docs/12-dast.md
    """
    # INTENTIONAL VULNERABILITY FOR LAB USE ONLY — do not copy this pattern.
    result = subprocess.run(  # noqa: S602
        f"echo {q}",
        shell=True,  # noqa: S602
        capture_output=True,
        text=True,
        timeout=5,
    )
    matches = [p for p in PRODUCTS if q.lower() in p["name"].lower()]
    return {
        "query": q,
        "count": len(matches),
        "items": matches,
        "_debug_echo": result.stdout.strip(),
    }


@app.get("/api/v1/debug")
def debug_info() -> dict[str, object]:
    """Return verbose internal state only when DEBUG_MODE env var is enabled.

    TEACHING NOTE: Exposing internal details behind a debug flag is a common
    misconfiguration. If DEBUG_MODE leaks into production (e.g. via a wrong
    ConfigMap patch), the endpoint exposes all environment variables including
    any secrets injected into the pod.
    This endpoint exists to teach env-gated information disclosure.
    See: k8s/base/configmap.yaml and k8s/nonprod/patches/configmap-patch.yaml
    """
    debug_enabled = os.getenv("DEBUG_MODE", "false").lower() == "true"
    if not debug_enabled:
        return {"debug": False, "message": "Debug mode is disabled."}

    # INTENTIONAL INFORMATION DISCLOSURE FOR LAB USE ONLY.
    return {
        "debug": True,
        "env": dict(os.environ),
        "products_in_memory": PRODUCTS,
        "internal_api_key_set": bool(INTERNAL_API_KEY),
    }


@app.get("/api/v1/random-pick")
def random_product() -> dict[str, object]:
    """Return a randomly selected product.

    TEACHING NOTE: random.random() is not cryptographically secure.
    For anything security-sensitive — tokens, voucher codes, session IDs —
    use the secrets module instead: secrets.choice(PRODUCTS).
    This endpoint exists so Semgrep rule python-insecure-random fires.
    See: docs/10-sast.md
    """
    # INTENTIONAL INSECURE RANDOM FOR LAB USE ONLY.
    index = int(random.random() * len(PRODUCTS))  # noqa: S311
    return {"picked": PRODUCTS[index]}
