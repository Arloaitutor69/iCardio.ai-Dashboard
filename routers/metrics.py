from fastapi import APIRouter, Query, HTTPException
from utils.metrics import (
    get_total_users,
    get_total_dicoms,
    get_dicoms_by_datasource,
    get_total_frames,
    get_frames_by_datasource,
    get_total_study_count,
    get_segmentations_by_type,
    get_total_segmentations
)

router = APIRouter()


@router.get("/api/metrics/total-users")
def total_users():
    try:
        return get_total_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/metrics/total-dicoms")
def total_dicoms(view: str = Query(default="total")):
    try:
        if view == "breakdown":
            return {"breakdown": get_dicoms_by_datasource()}
        return get_total_dicoms()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/metrics/total-frames")
def total_frames(view: str = Query(default="total")):
    try:
        if view == "breakdown":
            return {"breakdown": get_frames_by_datasource()}
        return get_total_frames()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/summary/total-studies")
def total_studies():
    try:
        return get_total_study_count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/metrics/total-segmentations")
def total_segmentations(view: str = Query(default="total")):
    try:
        if view == "breakdown":
            return {"breakdown": get_segmentations_by_type()}
        return get_total_segmentations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
