from fastapi import FastAPI
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

# Register all routers
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(labels.router)
app.include_router(meta.router)
app.include_router(review_status.router)
app.include_router(atlas.router)
app.include_router(dicoms.router)
