from flask import Blueprint, render_template, request, jsonify
from logic.abjad import calculate_abjad_value, get_numeric_symbolism
from logic.waffaq import recommend_waffaq_type, format_magic_square, detect_waffaq_type
from db.symbolism import get_planetary_info, get_extended_symbolism, get_matching_divine_names
from logic.text_analysis import extract_divine_names_from_text
from jinja2 import Template
import sqlite3

main_routes = Blueprint('main_routes', __name__)

def get_sections():
    conn = sqlite3.connect("instance/symbolism.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM html_sections WHERE visible = 1 ORDER BY section_order")
    result = cursor.fetchall()
    conn.close()
    return {name: content for name, content in result}

def render_section(template_str, context):
    template = Template(template_str)
    return template.render(**context)

def get_rendered_sections(context):
    conn = sqlite3.connect("instance/symbolism.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM html_sections WHERE visible = 1 ORDER BY section_order")
    result = cursor.fetchall()
    conn.close()

    rendered_sections = {}
    for name, content in result:
        rendered_sections[name] = render_section(content, context)
    return rendered_sections


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

    context = {
    "text": text,
    "value": value,
    "size": size,
    "multiplier": multiplier,
    "table": table,
    "waffaq_info": waffaq_info,
    "planet_info": planet_info,
    "extended_info": extended_info,
    "reduced_number": reduced_number,
    "number_meaning": number_meaning,
    "divine_matches": divine_matches
}
    sections = get_rendered_sections(context)


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
        divine_matches=divine_matches,
        sections=sections
    )
