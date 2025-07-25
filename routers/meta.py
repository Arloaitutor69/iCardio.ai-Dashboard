from fastapi import APIRouter, HTTPException
from utils.meta import (
    get_distinct_users,
    get_distinct_view_classes,
)

router = APIRouter()

@router.get("/api/users/distinct")
def users_distinct():
    try:
        return {"users": get_distinct_users()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/views/distinct")
def views_distinct():
    try:
        return {"view_classes": get_distinct_view_classes()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
