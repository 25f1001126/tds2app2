import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# YAML layer is empty

# .env layer
if os.getenv("APP_PORT"):
    config["port"] = int(os.getenv("APP_PORT"))

if os.getenv("APP_DEBUG"):
    config["debug"] = os.getenv("APP_DEBUG").lower() in (
        "true",
        "1",
        "yes",
        "on",
    )

if os.getenv("NUM_WORKERS"):
    config["workers"] = int(os.getenv("NUM_WORKERS"))

# Simulated OS environment layer (highest before CLI)
config["port"] = 8697
config["workers"] = 11
config["log_level"] = "warning"
config["api_key"] = "key-eelu4tjsrm"


def convert(key, value):
    if key in ("port", "workers"):
        return int(value)
    if key == "debug":
        return value.lower() in ("true", "1", "yes", "on")
    return value


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    result = config.copy()

    for item in set:
        if "=" in item:
            k, v = item.split("=", 1)
            result[k] = convert(k, v)

    result["api_key"] = "****"

    return result
