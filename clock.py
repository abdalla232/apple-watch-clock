import tkinter as tk
import math
from datetime import datetime

# ================= WINDOW =================
root = tk.Tk()
root.title("Responsive Apple Watch Clock")
root.configure(bg="black")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

scale = 1.0

# ================= SCALE CONTROL =================
def zoom_in(event=None):
    global scale
    scale += 0.1

def zoom_out(event=None):
    global scale
    global scale
    if scale > 0.3:
        scale -= 0.1

root.bind("<MouseWheel>", lambda e: zoom_in() if e.delta > 0 else zoom_out())

# ================= DRAW CLOCK =================
def draw_clock():

    canvas.delete("all")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # 🔥 CENTER ALWAYS
    cx = w // 2
    cy = h // 2

    radius = int(min(w, h) * 0.35 * scale)

    now = datetime.now()

    hour = now.hour % 12
    minute = now.minute
    second = now.second
    micro = now.microsecond

    # smooth movement
    sec = second + micro / 1_000_000
    min_total = minute + sec / 60
    hour_total = hour + min_total / 60

    # angles
    sa = math.radians(sec * 6 - 90)
    ma = math.radians(min_total * 6 - 90)
    ha = math.radians(hour_total * 30 - 90)

    # ================= OUTER GLOW =================
    for i in range(10):
        canvas.create_oval(
            cx - radius - i,
            cy - radius - i,
            cx + radius + i,
            cy + radius + i,
            outline="#1f1f1f"
        )

    # main circle
    canvas.create_oval(
        cx - radius,
        cy - radius,
        cx + radius,
        cy + radius,
        fill="#0a0a0a",
        outline="#2a2a2a",
        width=3
    )

    # ================= MARKS =================
    for i in range(60):
        ang = math.radians(i * 6 - 90)

        if i % 5 == 0:
            ln = 25
            col = "white"
            wline = 3
        else:
            ln = 12
            col = "#333333"
            wline = 1

        x1 = cx + math.cos(ang) * (radius - ln)
        y1 = cy + math.sin(ang) * (radius - ln)

        x2 = cx + math.cos(ang) * radius
        y2 = cy + math.sin(ang) * radius

        canvas.create_line(x1, y1, x2, y2, fill=col, width=wline)

    # ================= HANDS =================

    # hour
    hx = cx + math.cos(ha) * (radius * 0.5)
    hy = cy + math.sin(ha) * (radius * 0.5)

    canvas.create_line(cx, cy, hx, hy, fill="white", width=8, capstyle="round")

    # minute
    mx = cx + math.cos(ma) * (radius * 0.7)
    my = cy + math.sin(ma) * (radius * 0.7)

    canvas.create_line(cx, cy, mx, my, fill="#cccccc", width=5, capstyle="round")

    # second
    sx = cx + math.cos(sa) * (radius * 0.85)
    sy = cy + math.sin(sa) * (radius * 0.85)

    canvas.create_line(cx, cy, sx, sy, fill="#ff3b30", width=2)

    # center dot
    canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="white")

    # time text
    canvas.create_text(
        cx,
        cy + radius + 30,
        text=now.strftime("%H:%M:%S"),
        fill="white",
        font=("Arial", int(20 * scale), "bold")
    )

    root.after(16, draw_clock)

# ================= RESIZE EVENT =================
canvas.bind("<Configure>", lambda e: draw_clock())

draw_clock()
root.mainloop()