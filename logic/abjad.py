from db.connection import get_db_connection

# --- تحميل القيم الأبجدية من قاعدة البيانات ---
def get_abjad_values():
    conn = get_db_connection()
    rows = conn.execute("SELECT letter, value FROM abjad_values").fetchall()
    conn.close()
    return {row['letter']: row['value'] for row in rows}

abjad_values = get_abjad_values()

# --- حساب القيمة الأبجدية ---
def calculate_abjad_value(text):
    return sum(abjad_values.get(char, 0) for char in text)

# --- تقليل الرقم إلى رقم فردي ---
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

# --- الرمزية العددية ---
def get_number_meaning(n):
    conn = get_db_connection()
    row = conn.execute("SELECT meaning FROM number_symbolism WHERE number = ?", (n,)).fetchone()
    conn.close()
    return row['meaning'] if row else None

def get_numeric_symbolism(value):
    reduced = reduce_to_single_digit(value)
    meaning = get_number_meaning(reduced)
    return reduced, meaning
