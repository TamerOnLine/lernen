import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("instance/symbolism.db")  # غيّر المسار إذا لزم
cursor = conn.cursor()

# إنشاء جدول html_sections
cursor.execute("""
CREATE TABLE IF NOT EXISTS html_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    section_order INTEGER DEFAULT 0,
    visible BOOLEAN DEFAULT 1
);
""")

# حفظ التغييرات
conn.commit()
conn.close()

print("✅ تم إنشاء جدول html_sections بنجاح.")
