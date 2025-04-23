# Flask app to calculate abjad values and generate corresponding magic square using an external HTML template

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates')

# Mapping of Arabic letters to their abjad values
abjad_values = {
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5, 'ة': 5,
    'و': 6, 'ؤ': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10, 'ى': 10, 'ئ': 10, 'ی': 10,
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

def calculate_abjad_value(text):
    """
    Calculate the total abjad value of a given Arabic text.

    Args:
        text (str): Arabic text input.

    Returns:
        int: Sum of abjad values.
    """
    return sum(abjad_values.get(char, 0) for char in text)

def generate_odd_magic_square(n):
    """
    Generate an odd-sized magic square using the Siamese method.

    Args:
        n (int): Size of the square (must be odd).

    Returns:
        list[list[int]]: Generated magic square.
    """
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
    """
    Generate a doubly even magic square (size divisible by 4).

    Args:
        n (int): Size of the square (must be divisible by 4).

    Returns:
        list[list[int]]: Generated magic square.
    """
    square = [[(n * y) + x + 1 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i % 4 + j % 4) == 3):
                square[i][j] = (n * n + 1) - square[i][j]

    return square

def generate_singly_even_magic_square(n):
    """
    Generate a singly even magic square (size divisible by 2 but not 4).

    Args:
        n (int): Size of the square.

    Returns:
        list[list[int]]: Generated magic square.
    """
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
    """
    Determine the correct method to generate a magic square based on size.

    Args:
        n (int): Size of the magic square.

    Returns:
        list[list[int]]: Generated magic square.
    """
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)

def scale_magic_square(square, multiplier):
    """
    Multiply all elements of the magic square by a given multiplier.

    Args:
        square (list[list[int]]): Original magic square.
        multiplier (int): Multiplier value.

    Returns:
        list[list[int]]: Scaled magic square.
    """
    return [[val * multiplier for val in row] for row in square]

def recommend_waffaq_type(value):
    """
    Recommend a magic square size and multiplier to match a given abjad value.

    Args:
        value (int): Total abjad value.

    Returns:
        tuple: Recommended size, multiplier, and magic square.
    """
    for size in range(3, 20):
        cells = size * size
        if value % cells == 0:
            multiplier = value // cells
            square = generate_magic_square(size)
            scaled = scale_magic_square(square, multiplier)
            return size, multiplier, scaled

    return None, None, None

def format_magic_square(square):
    """
    Format the magic square into HTML table rows and cells.

    Args:
        square (list[list[int]]): Magic square to format.

    Returns:
        str: HTML representation of the magic square.
    """
    return "\n".join("<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>" for row in square)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Flask route for processing input text and rendering the result.

    Returns:
        str: Rendered HTML page with results.
    """
    text = request.form.get("text", "")
    value = size = multiplier = table = None

    if text:
        value = calculate_abjad_value(text)
        size, multiplier, square = recommend_waffaq_type(value)
        table = format_magic_square(square) if square else None

    return render_template(
        "index.html",
        text=text,
        value=value,
        size=size,
        multiplier=multiplier,
        table=table
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
        "magic_square": square
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
