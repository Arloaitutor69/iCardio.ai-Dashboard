from fastapi import APIRouter, Query
import requests
import os

router = APIRouter()

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

@router.get("/api/summary/enhanced-metric")
def get_enhanced_metric_data(endpoint: str = Query(...)):
    try:
        r = requests.get(f"{API_BASE}{endpoint}")
        data = r.json()
        if isinstance(data, dict):
            keys = ["total_users", "total_studies", "total_dicoms", "total_frames", "total_segmentations", "total", "count"]
            for key in keys:
                if key in data:
                    return {"total_all_time": data[key], "current_week": data.get("current_week", 0)}
            if "total_all_time" in data:
                return data
            elif len(data) == 1:
                return {"total_all_time": list(data.values())[0], "current_week": 0}
        elif isinstance(data, (int, float)):
            return {"total_all_time": data, "current_week": 0}
        return {"error": f"Unexpected response format: {type(data)}"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/api/labels/counts")
def get_label_counts(
    group_by: str = Query(...),
    user_filter: list[str] = Query(default=None),
    view_filter: list[str] = Query(default=None),
    time_range: str = Query(default=None)
):
    try:
        params = {
            "group_by": group_by,
            "user_filter": user_filter or [],
            "view_filter": view_filter or [],
            "time_range": time_range
        }
        r = requests.get(f"{API_BASE}/api/labels/counts", params=params)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@router.get("/api/users/distinct")
def get_distinct_users():
    try:
        r = requests.get(f"{API_BASE}/api/users/distinct")
        return r.json()
    except Exception as e:
        return {"users": []}

@router.get("/api/views/distinct")
def get_distinct_view_classes():
    try:
        r = requests.get(f"{API_BASE}/api/views/distinct")
        return r.json()
    except Exception as e:
        return {"view_classes": []}

@router.get("/api/review/data")
def get_review_data(endpoint: str = Query(...), interval_days: int = Query(None)):
    try:
        params = {}
        if interval_days:
            from datetime import datetime, timedelta
            today = datetime.utcnow().date()
            start_date = today - timedelta(days=interval_days)
            params["start_date"] = start_date.isoformat()
            params["end_date"] = today.isoformat()
        r = requests.get(f"{API_BASE}{endpoint}", params=params)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@router.get("/api/dicoms/filter-options")
def get_dicom_filter_options():
    try:
        r = requests.get(f"{API_BASE}/api/dicoms/filter-options")
        return r.json()
    except Exception as e:
        return {}

@router.get("/api/dicoms/breakdown")
def get_dicom_breakdown(
    datasource: list[str] = Query(default=None),
    manufacturer: list[str] = Query(default=None),
    model: list[str] = Query(default=None),
    type: list[str] = Query(default=None),
    has_media: bool = Query(default=None),
    flagged: bool = Query(default=None)
):
    try:
        params = {
            "datasource": datasource,
            "manufacturer": manufacturer,
            "model": model,
            "type": type,
            "has_media": has_media,
            "flagged": flagged
        }
        clean_params = {k: v for k, v in params.items() if v not in [None, [], ""]}
        r = requests.get(f"{API_BASE}/api/dicoms/breakdown", params=clean_params)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
