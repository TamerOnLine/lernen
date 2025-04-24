from db.connection import get_db_connection

def get_planetary_info(size):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM planetary_info WHERE size = ?", (size,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_extended_symbolism(size):
    conn = get_db_connection()
    row = conn.execute("SELECT meaning FROM extended_symbolism WHERE size = ?", (size,)).fetchone()
    conn.close()
    return row['meaning'] if row else None

def get_matching_divine_names(value, reduced_value=None):
    conn = get_db_connection()
    if reduced_value is not None:
        rows = conn.execute(
            "SELECT name, meaning FROM divine_names WHERE value = ? OR value = ?",
            (value, reduced_value)
        ).fetchall()
    else:
        rows = conn.execute("SELECT name, meaning FROM divine_names WHERE value = ?", (value,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
