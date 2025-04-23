import tkinter as tk
from tkinter import messagebox
import math

abjad_values = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4,
    'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ك': 20, 'ل': 30, 'م': 40,
    'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300,
    'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700,
    'ض': 800, 'ظ': 900, 'غ': 1000
}

def calculate_value(name):
    return sum(abjad_values.get(ch, 0) for ch in name)

def on_calculate():
    for widget in grid_frame.winfo_children():
        widget.destroy()

    name = entry.get().strip().replace(" ", "")
    if not name:
        messagebox.showwarning("تنبيه", "يرجى إدخال الاسم")
        return

    total = calculate_value(name)
    result_label.config(text=f"قيمة الاسم: {total}")

    size = min(math.ceil(math.sqrt(len(name))), 19)  # حتى 19x19 كحد أقصى

    for i in range(size * size):
        if i < len(name):
            ch = name[i]
            val = abjad_values.get(ch, 0)
            text = f"{ch}\n{val}"
        else:
            text = ""

        lbl = tk.Label(grid_frame, text=text, width=6, height=3, relief="ridge", font=("Arial", 9))
        lbl.grid(row=i // size, column=i % size, padx=1, pady=1)

# واجهة المستخدم
app = tk.Tk()
app.title("تطبيق الوفاق")
app.geometry("700x700")

tk.Label(app, text="أدخل الاسم أو العبارة:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(app, font=("Arial", 12), justify="center", width=40)
entry.pack(pady=5)

btn = tk.Button(app, text="احسب الوفاق", command=on_calculate, font=("Arial", 12))
btn.pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 14), fg="green")
result_label.pack(pady=5)

grid_frame = tk.Frame(app)
grid_frame.pack(pady=10)

app.mainloop()
