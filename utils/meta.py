from sqlalchemy import text
from utils.db import engine

def get_distinct_users():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT u.first_name || ' ' || u.last_name AS user_name
            FROM keypoint_collection_label kc
            JOIN "user" u ON kc.user_id = u.uuid
            WHERE u.first_name IS NOT NULL AND u.last_name IS NOT NULL
        """))
        return [row[0] for row in result]

def get_distinct_view_classes():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT vc.view
            FROM view_label vl
            JOIN view_class vc ON vl.view_class_id = vc.uuid
            WHERE vc.view IS NOT NULL
        """))
        return [row[0] for row in result]

