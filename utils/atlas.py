from sqlalchemy import text
from utils.db import engine

# ---------- Studies with DICOM Labeled ----------
def get_studies_with_dicom_labels():
    with open("queries/studies_with_dicoms.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(text(query)).scalar()
        return {"count": result}


# ---------- Studies with AI Predictions ----------
def get_predicted_study_count():
    with open("queries/studies_used.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        result = conn.execute(text(query)).scalar()
        return {"count": result}


# ---------- Fully Labeled Studies ----------
def get_fully_labeled_summary():
    with open("queries/fully_labeled_studies.sql", "r") as file:
        query = file.read().strip()
    with engine.connect() as conn:
        row = conn.execute(text(query)).fetchone()
        return {
            "fully_labeled_count": row[0],
            "total_studies": row[1],
            "percent_fully_labeled": float(row[2])
        }
