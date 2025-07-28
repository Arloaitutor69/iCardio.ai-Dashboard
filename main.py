from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import metrics, labels, meta, health, review_status, atlas, dicoms
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

# Register UUID support for psycopg2
psycopg2.extras.register_uuid()

app = FastAPI(
    title="iCardio Data API",
    description="FastAPI backend for metrics, labeling stats, and metadata queries",
    version="1.0.0"
)

# ✅ Enable CORS for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lovable.dev",
        "https://lovable.dev/projects/092e7b58-7a85-419a-88b5-df0619c05fbd"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all routers
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(labels.router)
app.include_router(meta.router)
app.include_router(review_status.router)
app.include_router(atlas.router)
app.include_router(dicoms.router)
