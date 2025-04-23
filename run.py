
import subprocess
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

abjad_values = {
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1,
    'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'ة': 5,
    'و': 6, 'ؤ': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ى': 10, 'ئ': 10, 'ی': 10,
    'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60,
    'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200,
    'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

def calculate_abjad_value(text):
    return sum(abjad_values.get(char, 0) for char in text)

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

@app.route("/", methods=["GET", "POST"])
def index():
    text = request.form.get("text", "")
    value = size = multiplier = table = None
    if text:
        value = calculate_abjad_value(text)
        size, multiplier, square = recommend_waffaq_type(value)
        table = format_magic_square(square) if square else None
    return render_template_string('\n<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n    <meta charset="UTF-8">\n    <title>Waffaq - توليد الوفق</title>\n    <style>\n        body { font-family: \'Arial\', sans-serif; text-align: center; direction: rtl; margin: 50px; }\n        textarea { width: 80%; height: 150px; max-width: 900px; font-size: 16px; padding: 10px; }\n        table { margin: 20px auto; border-collapse: collapse; }\n        td { border: 1px solid #000; padding: 10px; width: 50px; text-align: center; }\n    </style>\n</head>\n<body>\n    <h2>🔢 حساب القيمة العددية وتوليد المربع السحري</h2>\n    <p>اختر نصًا ثم اضغط احسب</p>\n    <form method="post">\n        <textarea name="text">{{ text or "" }}</textarea><br><br>\n        <button type="submit">احسب</button>\n    </form>\n    {% if value %}\n        <h3>📘 القيمة العددية: <span style="color:blue;">{{ value }}</span></h3>\n        {% if size and multiplier %}\n            <h4>📐 نوع الوفق: {{ size }}x{{ size }}</h4>\n            <h4>📊 معامل الضرب: {{ multiplier }}</h4>\n            <table>{{ table|safe }}</table>\n        {% endif %}\n    {% endif %}\n</body>\n</html>\n', text=text, value=value, size=size, multiplier=multiplier, table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
