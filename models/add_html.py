import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("instance/symbolism.db")
cursor = conn.cursor()

# قائمة الأقسام (name, content, order, visible)
sections = [
    ("intro_title", """
<h1>حساب الوفاق والقيمة الأبجدية</h1>
""", 1, True),

    ("form_section", """
<form method="POST">
  <textarea name="text" rows="2" cols="40" placeholder="أدخل النص هنا..." style="width: 500px; height: 200px;">{{ text }}</textarea><br>
  <button type="submit">احسب</button>
</form>
""", 2, True),

    ("result_summary", """
<div class="section">
  <h2>🔢 القيمة العددية والتحليل:</h2>
  <p><strong>النص:</strong> {{ text }}</p>
  <p><strong>القيمة الأبجدية:</strong> {{ value }}</p>
  <p><strong>الرقم المختزل:</strong> {{ reduced_number }}</p>
  <p><strong>الرمزية:</strong> {{ number_meaning }}</p>
</div>
""", 3, True),

    ("planetary_info", """
<div class="section">
  <h3>🔭 التحليل الفلكي:</h3>
  <p><strong>الكوكب:</strong> {{ planet_info.planet }}</p>
  <p><strong>اليوم:</strong> {{ planet_info.day }}</p>
  <p><strong>المعدن:</strong> {{ planet_info.metal }}</p>
  <p><strong>الوصف:</strong> {{ planet_info.description }}</p>
</div>
""", 4, True),

    ("extended_symbolism", """
<div class="section">
  <h3>🌌 الرمزية الموسعة:</h3>
  <p>{{ extended_info }}</p>
</div>
""", 5, True),

    ("waffaq_result", """
<div class="section">
  <h3>🧮 نوع الوفق:</h3>
  <p><strong>النوع:</strong> {{ waffaq_info.type }}</p>
  <ul>
    <li>الصفوف: <span class="{{ 'success' if waffaq_info.rows_ok else 'fail' }}">{{ '✔' if waffaq_info.rows_ok else '✘' }}</span></li>
    <li>الأعمدة: <span class="{{ 'success' if waffaq_info.cols_ok else 'fail' }}">{{ '✔' if waffaq_info.cols_ok else '✘' }}</span></li>
    <li>القطر: <span class="{{ 'success' if waffaq_info.diags_ok else 'fail' }}">{{ '✔' if waffaq_info.diags_ok else '✘' }}</span></li>
  </ul>
  {% if table %}
    <h4>الجدول:</h4>
    <table>{{ table|safe }}</table>
  {% else %}
    <p class="fail">⚠️ لا يمكن إنشاء مربع سحري متوافق مع هذه القيمة الأبجدية.</p>
  {% endif %}
</div>
""", 6, True),

    ("divine_names", """
<div class="section">
  <h3>🕊️ أسماء الله الحسنى المطابقة:</h3>
  <ul>
    {% if divine_matches|length > 0 %}
      {% for name in divine_matches %}
        <li><strong>{{ name.name }}</strong>: {{ name.meaning }}</li>
      {% endfor %}
    {% else %}
      <li>لا يوجد اسم مطابق في قاعدة البيانات لهذه القيمة الأبجدية.</li>
    {% endif %}
  </ul>
</div>
""", 7, True)
]

# إدخال أو تحديث الأقسام
for name, content, order, visible in sections:
    cursor.execute("""
        INSERT OR REPLACE INTO html_sections (id, name, content, section_order, visible)
        VALUES (
            (SELECT id FROM html_sections WHERE name = ?),
            ?, ?, ?, ?
        )
    """, (name, name, content.strip(), order, int(visible)))

# حفظ وإغلاق
conn.commit()
conn.close()
