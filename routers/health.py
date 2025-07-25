from fastapi import APIRouter
from utils.db import get_connection
import socket

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("/")
def health_check():
    try:
        # Try basic DB query
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()

        return {
            "status": "ok",
            "hostname": socket.gethostname(),
            "db_check": result[0],
        }

    except Exception as e:
        return {
            "status": "error",
            "hostname": socket.gethostname(),
            "error": str(e),
        }
