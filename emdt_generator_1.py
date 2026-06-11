import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random
import json
import csv
import os

# ══════════════════════════════════════════════════════
# COLOURS
# ══════════════════════════════════════════════════════
BG          = "#0a0f1e"   # main background — very dark navy
PANEL       = "#0d1b2e"   # frame background
CARD        = "#112240"   # card / treeview background
ACCENT      = "#00c9ff"   # cyan blue — main accent
ACCENT2     = "#0066cc"   # darker blue — buttons
BTN_HOVER   = "#0088ee"   # button hover
TEXT        = "#eb34ae"   #eb34ae
MUTED       = "#6b8caa"   # secondary text
GREEN       = "#00e676"   # export CSV button
PURPLE      = "#7c4dff"   # export JSON button
RED         = "#ff5252"   # clear button
BORDER      = "#1a3a5c"   # border colour

# ══════════════════════════════════════════════════════
# DATA GENERATORS
# ══════════════════════════════════════════════════════

def generate_battery():
    """Generates fake battery sensor data for EV testing."""
    return {
        "vehicle_id":      f"EV-{random.randint(1000, 9999)}",
        "soc_percent":     round(random.uniform(5.0, 100.0), 1),
        "voltage_v":       round(random.uniform(300.0, 420.0), 1),
        "current_a":       round(random.uniform(-200.0, 200.0), 1),
        "temperature_c":   round(random.uniform(-10.0, 45.0), 1),
        "health_percent":  round(random.uniform(70.0, 100.0), 1),
        "charge_cycles":   random.randint(0, 1500),
        "status":          random.choice(["Charging", "Driving", "Idle", "Standby"])
    }

def generate_charging_session():
    """Generates fake EV charging session data."""
    start_soc = round(random.uniform(5.0, 50.0), 1)
    end_soc   = round(random.uniform(start_soc + 10, 100.0), 1)
    return {
        "session_id":    f"CHG-{random.randint(1000, 9999)}",
        "vehicle_id":    f"EV-{random.randint(1000, 9999)}",
        "charger_type":  random.choice(["AC Level 1", "AC Level 2", "DC Fast", "DC Ultra-Fast"]),
        "location":      random.choice(["Lahti Campus", "City Center", "Highway A12", "Shopping Mall"]),
        "start_soc":     start_soc,
        "end_soc":       end_soc,
        "energy_kwh":    round(random.uniform(5.0, 80.0), 1),
        "duration_min":  random.randint(10, 180),
        "cost_eur":      round(random.uniform(2.0, 40.0), 2),
        "status":        random.choice(["Completed", "In Progress", "Failed"])
    }

def generate_powertrain():
    """Generates fake EV powertrain and motor data."""
    return {
        "vehicle_id":       f"EV-{random.randint(1000, 9999)}",
        "speed_kmh":        round(random.uniform(0.0, 130.0), 1),
        "motor_rpm":        random.randint(0, 8000),
        "torque_nm":        round(random.uniform(-300.0, 300.0), 1),
        "motor_temp_c":     round(random.uniform(20.0, 120.0), 1),
        "inverter_temp_c":  round(random.uniform(20.0, 90.0), 1),
        "efficiency_pct":   round(random.uniform(75.0, 98.0), 1),
        "regen_braking":    random.choice(["Yes", "No"]),
        "drive_mode":       random.choice(["Eco", "Normal", "Sport", "Regen+"])
    }

def generate_grid():
    """Generates fake power grid and energy data."""
    solar = round(random.uniform(0.0, 500.0), 1)
    wind  = round(random.uniform(0.0, 1000.0), 1)
    load  = round(random.uniform(200.0, 1500.0), 1)
    renewable_pct = round(min((solar + wind) / max(load, 1) * 100, 100.0), 1)
    return {
        "location":         random.choice(["Lahti Zone A", "Lahti Zone B", "Päijät-Häme"]),
        "solar_kw":         solar,
        "wind_kw":          wind,
        "grid_load_kw":     load,
        "ev_load_kw":       round(random.uniform(0.0, 300.0), 1),
        "renewable_pct":    renewable_pct,
        "co2_g_per_kwh":    round(random.uniform(20.0, 200.0), 1),
        "frequency_hz":     round(random.uniform(49.8, 50.2), 3),
        "grid_status":      random.choice(["Stable", "High Load", "Low Demand", "Peak"])
    }

def generate_trip():
    """Generates fake EV trip/journey data."""
    distance = round(random.uniform(1.0, 250.0), 1)
    energy   = round(distance * random.uniform(0.12, 0.30), 2)
    return {
        "trip_id":          f"TRIP-{random.randint(1000, 9999)}",
        "vehicle_id":       f"EV-{random.randint(1000, 9999)}",
        "vehicle_type":     random.choice(["Passenger Car", "Van", "Bus", "Cargo"]),
        "distance_km":      distance,
        "duration_min":     random.randint(5, 300),
        "avg_speed_kmh":    round(random.uniform(20.0, 100.0), 1),
        "energy_kwh":       energy,
        "regen_kwh":        round(energy * random.uniform(0.05, 0.25), 2),
        "co2_saved_kg":     round(distance * 0.12, 3),
        "route":            random.choice(["Urban", "Highway", "Mixed", "Rural"])
    }

# Map: data type → generator function + columns to show
GENERATORS = {
    "Battery Sensor": (generate_battery, [
        "vehicle_id", "soc_percent", "voltage_v", "current_a",
        "temperature_c", "health_percent", "charge_cycles", "status"
    ]),
    "Charging Session": (generate_charging_session, [
        "session_id", "vehicle_id", "charger_type", "location",
        "start_soc", "end_soc", "energy_kwh", "duration_min", "cost_eur", "status"
    ]),
    "Powertrain & Motor": (generate_powertrain, [
        "vehicle_id", "speed_kmh", "motor_rpm", "torque_nm",
        "motor_temp_c", "inverter_temp_c", "efficiency_pct", "regen_braking", "drive_mode"
    ]),
    "Grid & Energy": (generate_grid, [
        "location", "solar_kw", "wind_kw", "grid_load_kw",
        "ev_load_kw", "renewable_pct", "co2_g_per_kwh", "frequency_hz", "grid_status"
    ]),
    "Vehicle Trip": (generate_trip, [
        "trip_id", "vehicle_id", "vehicle_type", "distance_km",
        "duration_min", "avg_speed_kmh", "energy_kwh", "regen_kwh", "co2_saved_kg", "route"
    ]),
}

# ══════════════════════════════════════════════════════
# MAIN WINDOW
# ══════════════════════════════════════════════════════

root = tk.Tk()
root.title("⚡ EMDT Data Generator")
root.geometry("1000x720")
root.configure(bg=BG)
root.resizable(True, True)

# ── Tkinter style ──────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox",
    fieldbackground=CARD, background=CARD,
    foreground=TEXT, selectbackground=ACCENT,
    bordercolor=BORDER, arrowcolor=TEXT)
style.configure("Treeview",
    background=CARD, foreground=TEXT,
    fieldbackground=CARD, rowheight=26,
    bordercolor=BORDER)
style.configure("Treeview.Heading",
    background=ACCENT2, foreground=TEXT,
    font=("Consolas", 9, "bold"))
style.map("Treeview", background=[("selected", ACCENT2)])
style.configure("Vertical.TScrollbar",
    background=CARD, troughcolor=PANEL,
    arrowcolor=ACCENT)

# ══════════════════════════════════════════════════════
# BANNER IMAGE
# ══════════════════════════════════════════════════════

# Image file should be in the same folder as this script
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ev_banner.png")

try:
    img = Image.open(image_path)
    img = img.resize((1000, 200), Image.LANCZOS)  # resize to fit window
    banner_img = ImageTk.PhotoImage(img)
    banner_label = tk.Label(root, image=banner_img, bg=BG)
    banner_label.pack(fill="x")
except Exception:
    # If image not found, show a text banner instead
    banner_label = tk.Label(
        root,
        text="⚡  EMDT  —  Electric Mobility Digital Twin  —  Test Data Generator",
        bg=ACCENT2, fg=TEXT,
        font=("Consolas", 13, "bold"),
        pady=18
    )
    banner_label.pack(fill="x")

# ══════════════════════════════════════════════════════
# CONTROLS ROW
# ══════════════════════════════════════════════════════

controls = tk.Frame(root, bg=PANEL, pady=10)
controls.pack(fill="x", padx=0)

# Data type label + combobox
tk.Label(controls, text="Data Type:", bg=PANEL, fg=TEXT,
         font=("Consolas", 10)).grid(row=0, column=0, padx=(20, 6))

combo = ttk.Combobox(controls, width=22, state="readonly",
                     font=("Consolas", 10))
combo["values"] = list(GENERATORS.keys())
combo.current(0)
combo.grid(row=0, column=1, padx=(0, 20))

# Records label + spinbox
tk.Label(controls, text="Records:", bg=PANEL, fg=TEXT,
         font=("Consolas", 10)).grid(row=0, column=2, padx=(0, 6))

spinbox = tk.Spinbox(controls, from_=1, to=1000, width=6,
                     bg=CARD, fg=TEXT, insertbackground=TEXT,
                     buttonbackground=ACCENT2,
                     font=("Consolas", 10), relief="flat")
spinbox.grid(row=0, column=3, padx=(0, 20))

# ── Button helper ──────────────────────────────────────
def make_button(parent, text, color, cmd, col):
    btn = tk.Button(
        parent, text=text, bg=color, fg=BG,
        activebackground=BTN_HOVER, activeforeground=TEXT,
        font=("Consolas", 10, "bold"),
        relief="flat", padx=14, pady=6,
        cursor="hand2", command=cmd
    )
    btn.grid(row=0, column=col, padx=6)
    return btn

make_button(controls, "▶  Generate",  ACCENT,  lambda: generate(), 4)
make_button(controls, "✕  Clear",     RED,     lambda: clear(),    5)
make_button(controls, "💾  CSV",       GREEN,   lambda: export_csv(), 6)
make_button(controls, "{ }  JSON",    PURPLE,  lambda: export_json(), 7)

# ── Status bar ─────────────────────────────────────────
status_var = tk.StringVar(value="Ready — select a data type and click Generate.")
status_bar = tk.Label(root, textvariable=status_var,
                      bg=CARD, fg=MUTED,
                      font=("Consolas", 9), anchor="w", padx=16, pady=5)
status_bar.pack(fill="x")

# ══════════════════════════════════════════════════════
# TREEVIEW TABLE
# ══════════════════════════════════════════════════════

table_frame = tk.Frame(root, bg=BG)
table_frame.pack(fill="both", expand=True, padx=12, pady=(6, 0))

tree = ttk.Treeview(table_frame, show="headings", selectmode="browse")
scroll_y = ttk.Scrollbar(table_frame, orient="vertical",   command=tree.yview)
scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.pack(side="right",  fill="y")
scroll_x.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════

footer = tk.Label(root,
    text="EMDT-TDG  •  LAB University of Applied Sciences  •  Yeganeh Maleki  •  2026",
    bg=PANEL, fg=MUTED, font=("Consolas", 8), pady=6)
footer.pack(fill="x", side="bottom")

# ══════════════════════════════════════════════════════
# LOGIC
# ══════════════════════════════════════════════════════

generated_data = []

def generate():
    """Generate data and show it in the table."""
    global generated_data

    data_type = combo.get()
    count     = int(spinbox.get())
    gen_func, columns = GENERATORS[data_type]

    # Set up columns
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center", minwidth=80)

    # Clear old data
    tree.delete(*tree.get_children())
    generated_data = []

    # Generate new data
    for _ in range(count):
        row = gen_func()
        generated_data.append(row)
        tree.insert("", "end", values=[row[col] for col in columns])

    status_var.set(
        f"✓  {count} records generated  |  Type: {data_type}  |  "
        f"Columns: {len(columns)}  |  Ready to export."
    )

def clear():
    """Clear the table."""
    tree.delete(*tree.get_children())
    tree["columns"] = []
    generated_data.clear()
    status_var.set("Cleared.")

def export_csv():
    """Export generated data to a CSV file."""
    if not generated_data:
        messagebox.showwarning("No Data", "Please generate data first!")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save as CSV"
    )
    if not path:
        return
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=generated_data[0].keys())
        writer.writeheader()
        writer.writerows(generated_data)
    messagebox.showinfo("✓ Saved", f"CSV file saved:\n{path}")
    status_var.set(f"✓  CSV exported → {path}")

def export_json():
    """Export generated data to a JSON file."""
    if not generated_data:
        messagebox.showwarning("No Data", "Please generate data first!")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save as JSON"
    )
    if not path:
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(generated_data, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("✓ Saved", f"JSON file saved:\n{path}")
    status_var.set(f"✓  JSON exported → {path}")

# ══════════════════════════════════════════════════════
root.mainloop()
