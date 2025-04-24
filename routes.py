from flask import Blueprint, render_template, request, jsonify
from logic.abjad import calculate_abjad_value, get_numeric_symbolism
from logic.waffaq import recommend_waffaq_type, format_magic_square, detect_waffaq_type
from db.symbolism import get_planetary_info, get_extended_symbolism, get_matching_divine_names

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=['GET', 'POST'])
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

@main_routes.route('/api/waffaq', methods=['POST'])
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
