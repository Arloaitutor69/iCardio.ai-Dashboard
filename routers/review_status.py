
from fastapi import APIRouter, Query, HTTPException
from utils.review_status import (
    get_pending_vs_completed_reviews,
    get_reviewers_active,
    get_acceptance_rate_by_reviewer
)

router = APIRouter()


@router.get("/api/review/pending-vs-completed")
def pending_vs_completed_reviews(
    start_date: str = Query(default=None),
    end_date: str = Query(default=None)
):
    try:
        data = get_pending_vs_completed_reviews(
            start_date=start_date,
            end_date=end_date
        )
        return {"breakdown": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/review/active-reviewers")
def active_reviewers(
    activity_interval_days: int = Query(default=None)
):
    try:
        data = get_reviewers_active(activity_interval_days=activity_interval_days)
        return {"reviewers": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/review/acceptance-rate")
def acceptance_rate_by_reviewer(
    interval_days: int = Query(default=None)
):
    try:
        data = get_acceptance_rate_by_reviewer(interval_days=interval_days)
        return {"breakdown": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
