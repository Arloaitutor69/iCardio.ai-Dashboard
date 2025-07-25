from fastapi import APIRouter, Query, HTTPException
from utils.labels import get_label_counts_df

router = APIRouter()

@router.get("/api/labels/counts")
def get_label_counts(
    group_by: str = Query("user", enum=["user", "date", "user_and_date"]),
    view_filter: list[str] = Query(default=None),
    user_filter: list[str] = Query(default=None),
    time_range: str = Query(default=None, enum=["1w", "2w", "1m", "6m", "1y", "5y"])
):
    try:
        df = get_label_counts_df(group_by, view_filter, user_filter, time_range)
        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
