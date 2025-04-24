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
