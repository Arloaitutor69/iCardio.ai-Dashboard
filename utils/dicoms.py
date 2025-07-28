from sqlalchemy import text
from utils.db import engine

def get_dicom_breakdown(
    datasource: list[str] = None,
    manufacturer: list[str] = None,
    model: list[str] = None,
    type: list[str] = None,
    has_media: bool = None,
    flagged: bool = None
):
    with open("queries/dicoms_breakdown.sql", "r") as file:
        query = text(file.read().strip())

    def normalize(value):
        return value if value else None

    with engine.connect() as conn:
        result = conn.execute(query, {
            "datasource": normalize(datasource),
            "manufacturer": normalize(manufacturer),
            "model": normalize(model),
            "type": normalize(type),
            "has_media": has_media,
            "flagged": flagged
        }).fetchall()

        return [dict(row._mapping) for row in result]

def get_all_filter_options():
    with engine.connect() as conn:
        result = {}

        result["datasource"] = [row[0] for row in conn.execute(text("""
            SELECT DISTINCT ds.name
            FROM dicom d
            JOIN study s ON d.study_id = s.uuid
            JOIN datasource ds ON s.datasource_id = ds.uuid
            WHERE ds.name IS NOT NULL
            ORDER BY ds.name
        """))]

        result["manufacturer"] = [row[0] for row in conn.execute(text("""
            SELECT DISTINCT manufacturer
            FROM dicom
            WHERE manufacturer IS NOT NULL
            ORDER BY manufacturer
        """))]

        result["model"] = [row[0] for row in conn.execute(text("""
            SELECT DISTINCT manufacturer_model_name
            FROM dicom
            WHERE manufacturer_model_name IS NOT NULL
            ORDER BY manufacturer_model_name
        """))]

        result["type"] = [row[0] for row in conn.execute(text("""
            SELECT DISTINCT type
            FROM dicom
            WHERE type IS NOT NULL
            ORDER BY type
        """))]

        return result
