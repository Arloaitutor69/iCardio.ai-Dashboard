from fastapi import APIRouter, HTTPException
from utils.atlas import (
    get_studies_with_dicom_labels,
    get_predicted_study_count,
    get_fully_labeled_summary
)

router = APIRouter()

@router.get("/api/atlas/dicom-labeled-studies")
def dicom_labeled_studies():
    try:
        return get_studies_with_dicom_labels()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/atlas/predicted-studies")
def predicted_studies():
    try:
        return get_predicted_study_count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/atlas/fully-labeled-summary")
def fully_labeled_summary():
    try:
        return get_fully_labeled_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
