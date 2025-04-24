from db.connection import get_db_connection

def extract_divine_names_from_text(text):
    conn = get_db_connection()
    rows = conn.execute("SELECT name, value FROM divine_names").fetchall()
    conn.close()
    
    found = []
    for row in rows:
        if row['name'] in text:
            found.append({'name': row['name'], 'value': row['value']})
    return found
