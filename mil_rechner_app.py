__version__ = "1.0.0"
import os
import bisect
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Pillow-Import für skalierbares Hintergrundbild
try:
    from PIL import Image, ImageTk
    from PIL.Image import Resampling
except ImportError:
    Image = ImageTk = Resampling = None

# Datenbasis
distances = [30, 75, 100, 150, 200, 300, 400, 500, 550]
mils      = [1975, 1800, 1750, 1640, 1550, 1420, 1270, 1115, 800]

def meters_to_mil(m):
    if m <= distances[0]:
        return mils[0] / 1000
    if m >= distances[-1]:
        return mils[-1] / 1000
    idx = bisect.bisect_left(distances, m)
    x0, x1 = distances[idx-1], distances[idx]
    y0, y1 = mils[idx-1], mils[idx]
    val = y0 + (y1 - y0) * (m - x0) / (x1 - x0)
    return val / 1000

def set_background(root):
    """Wenn background.png existiert, lade es und skaliere es bei Fenster-Resize."""
    if Image and os.path.exists("background.png"):
        original = Image.open("background.png")
        bg_label = tk.Label(root)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        def resize_bg(event):
            w, h = event.width, event.height
            # Resampling.LANCZOS statt ANTIALIAS
            resized = original.resize((w, h), Resampling.LANCZOS)
            bg_img = ImageTk.PhotoImage(resized)
            bg_label.img = bg_img
            bg_label.config(image=bg_img)

        root.bind("<Configure>", resize_bg)
        bg_label.lower()

# Hauptfenster
root = tk.Tk()
root.title("🎯 Mil-Rechner für Schützen")
root.geometry("400x200")
root.configure(bg="#1e1e2f")

set_background(root)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 12))
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("Transparent.TButton",
    relief="flat", borderwidth=0,
    background="#1e1e2f", foreground="white", font=("Segoe UI", 11)
)
style.map("Transparent.TButton",
    background=[("active", "#1e1e2f"), ("pressed", "#1e1e2f")],
    foreground=[("active", "white"), ("pressed", "white")]
)

title_label = ttk.Label(root, text="🔭 Meter → Mil Umrechner", font=("Segoe UI", 14, "bold"))
title_label.pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=5)
ttk.Label(frame, text="Entfernung (m):").grid(row=0, column=0, padx=5)
entry = ttk.Entry(frame, width=10)
entry.grid(row=0, column=1, padx=5)

result_var = tk.StringVar(value="Mil: –")
result_label = ttk.Label(root, textvariable=result_var)
result_label.pack(pady=10)

def on_convert():
    try:
        m = float(entry.get())
        mil = meters_to_mil(m)
        result_var.set(f"Mil: {mil:.3f}")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

convert_btn = ttk.Button(root, text="Berechnen", command=on_convert, style="Transparent.TButton")
convert_btn.pack()

footer = ttk.Label(root, text="© Dev's Mörser Tool", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=5)

root.mainloop()