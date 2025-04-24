
from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__, template_folder='templates')

# --- اتصال بقاعدة البيانات ---
def get_db_connection():
    db_path = os.path.join('instance', 'symbolism.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- استيراد القيم الأبجدية من القاعدة ---
def get_abjad_values():
    conn = get_db_connection()
    rows = conn.execute("SELECT letter, value FROM abjad_values").fetchall()
    conn.close()
    return {row['letter']: row['value'] for row in rows}

abjad_values = get_abjad_values()

# --- الرمزية العددية المفردة من القاعدة ---
def get_number_meaning(n):
    conn = get_db_connection()
    row = conn.execute("SELECT meaning FROM number_symbolism WHERE number = ?", (n,)).fetchone()
    conn.close()
    return row['meaning'] if row else None

# --- الرمزية الموسعة من القاعدة ---
def get_extended_symbolism(size):
    conn = get_db_connection()
    row = conn.execute("SELECT meaning FROM extended_symbolism WHERE size = ?", (size,)).fetchone()
    conn.close()
    return row['meaning'] if row else None

# --- البيانات الفلكية من القاعدة ---
def get_planetary_info(size):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM planetary_info WHERE size = ?", (size,)).fetchone()
    conn.close()
    return dict(row) if row else None

# --- أسماء الله الحسنى التي تطابق القيمة الأبجدية أو المختزلة ---
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

# --- حساب القيمة الأبجدية ---
def calculate_abjad_value(text):
    return sum(abjad_values.get(char, 0) for char in text)

# --- تقليل الرقم إلى رقم فردي ---
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def get_numeric_symbolism(value):
    reduced = reduce_to_single_digit(value)
    meaning = get_number_meaning(reduced)
    return reduced, meaning

# --- المربعات السحرية (وفق) ---
def generate_odd_magic_square(n):
    square = [[0] * n for _ in range(n)]
    num, i, j = 1, 0, n // 2
    while num <= n * n:
        square[i][j] = num
        num += 1
        newi, newj = (i - 1) % n, (j + 1) % n
        if square[newi][newj]:
            i += 1
        else:
            i, j = newi, newj
    return square

def generate_doubly_even_magic_square(n):
    square = [[(n * y) + x + 1 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i % 4 + j % 4) == 3):
                square[i][j] = (n * n + 1) - square[i][j]
    return square

def generate_singly_even_magic_square(n):
    half = n // 2
    sub = generate_odd_magic_square(half)
    square = [[0] * n for _ in range(n)]
    add = [0, 2, 3, 1]
    for i in range(half):
        for j in range(half):
            for k in range(4):
                r = i + (k // 2) * half
                c = j + (k % 2) * half
                square[r][c] = sub[i][j] + add[k] * half * half
    k = (n - 2) // 4
    for i in range(n):
        for j in range(n):
            if (i < half and (j < k or j >= n - k)) or (i >= half and (k <= j < n - k)):
                if not (i == half and j == k):
                    square[i][j], square[i - half][j] = square[i - half][j], square[i][j]
    return square

def generate_magic_square(n):
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)

def scale_magic_square(square, multiplier):
    return [[val * multiplier for val in row] for row in square]

def recommend_waffaq_type(value):
    for size in range(3, 20):
        cells = size * size
        if value % cells == 0:
            multiplier = value // cells
            square = generate_magic_square(size)
            scaled = scale_magic_square(square, multiplier)
            return size, multiplier, scaled
    return None, None, None

def format_magic_square(square):
    return "\n".join("<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>" for row in square)

def detect_waffaq_type(square):
    if not square:
        return {"type": "غير موجود", "rows_ok": False, "cols_ok": False, "diags_ok": False}
    n = len(square)
    expected_sum = sum(square[0])
    rows_ok = all(sum(row) == expected_sum for row in square)
    cols_ok = all(sum(square[i][j] for i in range(n)) == expected_sum for j in range(n))
    diag1 = sum(square[i][i] for i in range(n))
    diag2 = sum(square[i][n - 1 - i] for i in range(n))
    diags_ok = diag1 == expected_sum and diag2 == expected_sum

    if rows_ok and cols_ok and diags_ok:
        w_type = "تام"
    elif (rows_ok and cols_ok) or (rows_ok and diags_ok) or (cols_ok and diags_ok):
        w_type = "جزئي"
    elif rows_ok or cols_ok or diags_ok:
        w_type = "ضعيف"
    else:
        w_type = "غير موجود"

    return {"type": w_type, "rows_ok": rows_ok, "cols_ok": cols_ok, "diags_ok": diags_ok}

@app.route('/', methods=['GET', 'POST'])
def index():
    text = request.form.get("text", "")
    value = size = multiplier = table = reduced_number = number_meaning = None
    waffaq_info = {"type": "غير موجود", "rows_ok": False, "cols_ok": False, "diags_ok": False}
    divine_matches = []

    if text:
        value = calculate_abjad_value(text)
        reduced_number, number_meaning = get_numeric_symbolism(value)
        size, multiplier, square = recommend_waffaq_type(value)
        table = format_magic_square(square) if square else None
        waffaq_info = detect_waffaq_type(square) if square else waffaq_info
        planet_info = get_planetary_info(size) if size else None
        extended_info = get_extended_symbolism(size) if size and size > 9 else None
        divine_matches = get_matching_divine_names(value, reduced_number)
    else:
        planet_info = extended_info = reduced_number = number_meaning = None

    return render_template(
        "index.html",
        text=text,
        value=value,
        size=size,
        multiplier=multiplier,
        table=table,
        waffaq_info=waffaq_info,
        planet_info=planet_info,
        extended_info=extended_info,
        reduced_number=reduced_number,
        number_meaning=number_meaning,
        divine_matches=divine_matches
    )

@app.route('/api/waffaq', methods=['POST'])
def api_waffaq():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "يرجى إرسال نص"}), 400
    value = calculate_abjad_value(text)
    size, multiplier, square = recommend_waffaq_type(value)
    return jsonify({
        "abjad_value": value,
        "size": size,
        "multiplier": multiplier,
        "magic_square": square,
        "waffaq_type": detect_waffaq_type(square)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
