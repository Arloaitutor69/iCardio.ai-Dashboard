from sqlalchemy import text
from utils.db import engine, get_connection

# Helper for 2-column return
def fetch_total_and_weekly(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query)).fetchone()
        return {
            "total_all_time": result[0],
            "current_week": result[1]
        }

# ---------- Total Users ----------
def get_total_users():
    with open("queries/total_users.sql", "r") as file:
        query = file.read().strip()
    return fetch_total_and_weekly(query)

# ---------- Total DICOMs ----------
def get_total_dicoms():
    with open("queries/total_dicoms.sql", "r") as file:
        query = file.read().strip()
    return fetch_total_and_weekly(query)

# ---------- DICOMs by Datasource ----------
def get_dicoms_by_datasource():
    with open("queries/dicoms_by_datasource.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{"group_key": row[0], "value": row[1]} for row in result.fetchall()]

# ---------- Total Frames ----------
def get_total_frames():
    with open("queries/total_frames.sql", "r") as file:
        query = file.read().strip()
    return fetch_total_and_weekly(query)

# ---------- Frames by Datasource ----------
def get_frames_by_datasource():
    with open("queries/frames_by_datasource.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{"group_key": row[0], "value": row[1]} for row in result.fetchall()]

# ---------- Total Studies ----------
def get_total_study_count():
    with open("queries/total_study_count.sql", "r") as file:
        query = file.read().strip()
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            return {
                "total_all_time": row[0],
                "current_week": row[1]
            }

# ---------- Total Segmentations ----------
def get_total_segmentations():
    with open("queries/total_segmentations.sql", "r") as file:
        query = file.read().strip()
    return fetch_total_and_weekly(query)

# ---------- Segmentations Breakdown by Type ----------
def get_segmentations_by_type():
    with open("queries/segmentations_by_type.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{"group_key": row[0], "value": row[1]} for row in result.fetchall()]
