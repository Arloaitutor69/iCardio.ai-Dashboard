import pandas as pd
from sqlalchemy import text
from utils.db import engine
from datetime import datetime, timedelta

def get_label_counts_df(group_by: str, view_filter: list[str], user_filter: list[str], time_range: str) -> pd.DataFrame:
    group_by_map = {
        "user": "label_counts_by_user.sql",
        "date": "label_counts_by_date.sql",
        "user_and_date": "label_counts_by_user_and_date.sql"
    }

    if group_by not in group_by_map:
        raise ValueError("Invalid group_by value. Use 'user', 'date', or 'user_and_date'.")

    query_file = f"queries/{group_by_map[group_by]}"
    sql = open(query_file).read()

    if time_range:
        days_map = {
            "1w": 7, "2w": 14, "1m": 30, "6m": 180, "1y": 365, "5y": 1825
        }
        since = datetime.today() - timedelta(days=days_map.get(time_range, 0))
    else:
        since = None

    params = {
        "view_filter": view_filter if view_filter else None,
        "user_filter": user_filter if user_filter else None,
        "since": since
    }

    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)
