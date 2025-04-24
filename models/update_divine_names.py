import sys
import os

# إضافة مجلد المشروع الرئيسي إلى sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)


import sqlite3
import json
from logic.abjad import calculate_abjad_value
from logic.waffaq import recommend_waffaq_type
from db.connection import get_db_connection

def update_divine_names_with_waffaq():
    conn = get_db_connection()
    cur = conn.cursor()

    # التأكد من الأعمدة المطلوبة
    cur.execute("PRAGMA table_info(divine_names)")
    existing_columns = [row["name"] for row in cur.fetchall()]
    columns_to_add = {
        "abjad_value": "INTEGER",
        "waffaq_size": "INTEGER",
        "waffaq_multiplier": "INTEGER",
        "waffaq_data": "TEXT"
    }
    for col, col_type in columns_to_add.items():
        if col not in existing_columns:
            cur.execute(f"ALTER TABLE divine_names ADD COLUMN {col} {col_type}")

    # استرجاع كل الأسماء
    cur.execute("SELECT name FROM divine_names")
    names = [row["name"] for row in cur.fetchall()]

    # تحديث كل اسم
    for name in names:
        abjad_value = calculate_abjad_value(name)
        size, multiplier, square = recommend_waffaq_type(abjad_value)
        waffaq_data = json.dumps(square) if square else None

        cur.execute("""
            UPDATE divine_names
            SET abjad_value = ?, waffaq_size = ?, waffaq_multiplier = ?, waffaq_data = ?
            WHERE name = ?
        """, (abjad_value, size, multiplier, waffaq_data, name))

    conn.commit()
    conn.close()
    print("✅ تم تحديث أسماء الله الحسنى بالقيم الجديدة بنجاح.")

if __name__ == "__main__":
    update_divine_names_with_waffaq()
