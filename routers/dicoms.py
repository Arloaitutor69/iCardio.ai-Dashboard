from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from utils.dicoms import get_dicom_breakdown

router = APIRouter()

@router.get("/api/dicoms/breakdown")
def dicom_breakdown(
    datasource: Optional[List[str]] = Query(default=None),
    manufacturer: Optional[List[str]] = Query(default=None),
    model: Optional[List[str]] = Query(default=None),
    type: Optional[List[str]] = Query(default=None),
    has_media: Optional[bool] = Query(default=None),
    flagged: Optional[bool] = Query(default=None)
):
    try:
        data = get_dicom_breakdown(
            datasource=datasource,
            manufacturer=manufacturer,
            model=model,
            type=type,
            has_media=has_media,
            flagged=flagged
        )
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/dicoms/filter-options")
def dicom_filter_options():
    try:
        from utils.dicoms import get_all_filter_options
        options = get_all_filter_options()
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
