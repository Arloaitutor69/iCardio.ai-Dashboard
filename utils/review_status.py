
from sqlalchemy import text
from utils.db import engine
from datetime import datetime, timedelta


# ---------- Pending vs Completed Reviews ----------
def get_pending_vs_completed_reviews(start_date=None, end_date=None):
    with open("queries/pending_vs_completed_reviews.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {
                "start_date": start_date,
                "end_date": end_date,
            }
        )
        return [{"group_key": row[0], "value": row[1]} for row in result.fetchall()]

# ---------- Reviewers Active ----------
def get_reviewers_active(activity_interval_days=None):
    with open("queries/reviewers_active.sql", "r") as file:
        query = file.read().strip()

    if activity_interval_days is not None:
        cutoff_time = datetime.now() - timedelta(days=activity_interval_days)
    else:
        cutoff_time = None

    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {"cutoff_time": cutoff_time}
        )
        return [
            {"group_key": row[0], "value": row[1], "last_review_time": str(row[2])}
            for row in result.fetchall()
        ]


# ---------- Acceptance Rate by Reviewer ----------
def get_acceptance_rate_by_reviewer(interval_days=None):
    with open("queries/acceptance_rate_by_reviewer.sql", "r") as file:
        query = file.read().strip()

    if interval_days is not None:
        cutoff_time = datetime.now() - timedelta(days=interval_days)
    else:
        cutoff_time = None

    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {"cutoff_time": cutoff_time}
        )
        return [
            {"group_key": row[0], "sub_group": row[1], "value": row[2]}
            for row in result.fetchall()
        ]
