"""
EMDT Test Data Generator

Electric Mobility Digital Twin (EMDT)
LAB University of Applied Sciences — Yeganeh Maleki, 2026
"""

from __future__ import annotations

import csv
import json
import random
import sqlite3
import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from PIL import Image, ImageTk

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Theme:
    """Colour palette and typography."""

    bg: str = "#0a0f1e"
    panel: str = "#0d1b2e"
    card: str = "#112240"
    accent: str = "#00c9ff"
    accent_secondary: str = "#0066cc"
    btn_hover: str = "#0088ee"
    text: str = "#eb34ae"
    muted: str = "#6b8caa"
    green: str = "#00e676"
    purple: str = "#7c4dff"
    orange: str = "#ff9800"
    red: str = "#ff5252"
    border: str = "#1a3a5c"

    font_family: str = "Consolas"
    font_size: int = 10
    font_size_small: int = 9
    font_size_title: int = 12
    font_size_banner: int = 13

    @property
    def font(self) -> tuple[str, int]:
        return (self.font_family, self.font_size)

    @property
    def font_bold(self) -> tuple[str, int, str]:
        return (self.font_family, self.font_size, "bold")

    @property
    def font_small(self) -> tuple[str, int]:
        return (self.font_family, self.font_size_small)

    @property
    def font_title(self) -> tuple[str, int, str]:
        return (self.font_family, self.font_size_title, "bold")


THEME = Theme()

BANNER_FILE_ALIASES = (
    "ev_banner.png",
    "ev_banner_1.png",
    "ChatGPT Image Jun 10, 2026, 10_08_52 AM.png",
)


def find_banner_path() -> Path | None:
    """Look for the banner image next to this script and in the working directory."""
    search_dirs: list[Path] = []
    for directory in (Path(__file__).resolve().parent, Path.cwd()):
        if directory not in search_dirs:
            search_dirs.append(directory)

    for directory in search_dirs:
        for name in BANNER_FILE_ALIASES:
            candidate = directory / name
            if candidate.is_file():
                return candidate
    return None


WINDOW_SIZE = "1000x720"
BANNER_SIZE = (1000, 200)
MAX_RECORDS = 1000
MIN_RECORDS = 1
COLUMN_WIDTH = 130
COLUMN_MIN_WIDTH = 80

# ---------------------------------------------------------------------------
# Data generators
# ---------------------------------------------------------------------------

Record = dict[str, Any]
GeneratorFunc = Callable[[], Record]

MODELS = ("Model 3 Standard", "Model 3 Long Range", "Model 3 Performance")


def _vehicle_id() -> str:
    return f"EV-{random.randint(1000, 9999)}"


def generate_battery() -> Record:
    """Generate Tesla Model 3 battery sensor readings."""
    return {
        "vehicle_id": _vehicle_id(),
        "model": random.choice(MODELS),
        "soc_percent": round(random.uniform(20.0, 80.0), 1),
        "voltage_v": round(random.uniform(340.0, 400.0), 1),
        "current_a": round(random.uniform(-200.0, 200.0), 1),
        "capacity_kwh": random.choice([50, 62, 75, 82]),
        "temperature_c": round(random.uniform(-10.0, 45.0), 1),
        "health_percent": round(random.uniform(70.0, 100.0), 1),
        "charge_cycles": random.randint(0, 1200),
        "status": random.choice(["Charging", "Driving", "Idle", "Standby"]),
    }


def generate_charging_session() -> Record:
    """Generate Tesla Model 3 charging session data."""
    start_soc = round(random.uniform(10.0, 40.0), 1)
    end_soc = round(random.uniform(max(start_soc + 5.0, 60.0), 90.0), 1)
    return {
        "session_id": f"CHG-{random.randint(1000, 9999)}",
        "vehicle_id": _vehicle_id(),
        "model": random.choice(MODELS),
        "charger_type": random.choice([
            "AC Level 2 - 11kW",
            "DC Supercharger V2 - 150kW",
            "DC Supercharger V3 - 250kW",
        ]),
        "location": random.choice([
            "Lahti Supercharger",
            "Helsinki Supercharger",
            "Home Charger",
            "Shopping Mall",
        ]),
        "start_soc": start_soc,
        "end_soc": end_soc,
        "energy_kwh": round(random.uniform(10.0, 75.0), 1),
        "duration_min": random.randint(15, 480),
        "cost_eur": round(random.uniform(3.0, 35.0), 2),
        "status": random.choice(["Completed", "In Progress", "Interrupted"]),
    }


def generate_powertrain() -> Record:
    """Generate Tesla Model 3 powertrain and motor data."""
    return {
        "vehicle_id": _vehicle_id(),
        "model": random.choice(MODELS),
        "speed_kmh": round(random.uniform(0.0, 261.0), 1),
        "motor_rpm": random.randint(0, 19000),
        "torque_nm": round(random.uniform(0.0, 493.0), 1),
        "motor_temp_c": round(random.uniform(20.0, 120.0), 1),
        "inverter_temp_c": round(random.uniform(20.0, 90.0), 1),
        "efficiency_pct": round(random.uniform(75.0, 98.0), 1),
        "regen_braking": random.choice(["Yes", "No"]),
        "drive_mode": random.choice(["Eco", "Normal", "Sport", "Track"]),
    }


def generate_grid() -> Record:
    """Generate regional power grid and energy mix data."""
    solar = round(random.uniform(0.0, 500.0), 1)
    wind = round(random.uniform(0.0, 1000.0), 1)
    load = round(random.uniform(200.0, 1500.0), 1)
    renewable_pct = round(min((solar + wind) / max(load, 1) * 100, 100.0), 1)
    return {
        "location": random.choice(["Lahti Zone A", "Lahti Zone B", "Päijät-Häme"]),
        "solar_kw": solar,
        "wind_kw": wind,
        "grid_load_kw": load,
        "ev_load_kw": round(random.uniform(0.0, 300.0), 1),
        "renewable_pct": renewable_pct,
        "co2_g_per_kwh": round(random.uniform(20.0, 200.0), 1),
        "frequency_hz": round(random.uniform(49.8, 50.2), 3),
        "grid_status": random.choice(["Stable", "High Load", "Low Demand", "Peak"]),
    }


def generate_trip() -> Record:
    """Generate Tesla Model 3 trip telemetry."""
    distance = round(random.uniform(1.0, 600.0), 1)
    energy = round(distance * random.uniform(0.12, 0.20), 2)
    return {
        "trip_id": f"TRIP-{random.randint(1000, 9999)}",
        "vehicle_id": _vehicle_id(),
        "vehicle_type": random.choice(["Passenger Car", "Van", "Bus", "Cargo"]),
        "distance_km": distance,
        "duration_min": random.randint(5, 300),
        "avg_speed_kmh": round(random.uniform(20.0, 130.0), 1),
        "energy_kwh": energy,
        "regen_kwh": round(energy * random.uniform(0.05, 0.25), 2),
        "co2_saved_kg": round(distance * 0.12, 3),
        "route": random.choice(["Urban", "Highway", "Mixed", "Rural"]),
    }


@dataclass(frozen=True)
class DataTypeSpec:
    """Maps a label to its generator and table columns."""

    label: str
    generator: GeneratorFunc
    columns: tuple[str, ...]


DATA_TYPES: tuple[DataTypeSpec, ...] = (
    DataTypeSpec(
        "Battery Sensor",
        generate_battery,
        (
            "vehicle_id", "soc_percent", "voltage_v", "current_a",
            "temperature_c", "health_percent", "charge_cycles", "status",
        ),
    ),
    DataTypeSpec(
        "Charging Session",
        generate_charging_session,
        (
            "session_id", "vehicle_id", "charger_type", "location",
            "start_soc", "end_soc", "energy_kwh", "duration_min", "cost_eur", "status",
        ),
    ),
    DataTypeSpec(
        "Powertrain & Motor",
        generate_powertrain,
        (
            "vehicle_id", "speed_kmh", "motor_rpm", "torque_nm",
            "motor_temp_c", "inverter_temp_c", "efficiency_pct", "regen_braking", "drive_mode",
        ),
    ),
    DataTypeSpec(
        "Grid & Energy",
        generate_grid,
        (
            "location", "solar_kw", "wind_kw", "grid_load_kw",
            "ev_load_kw", "renewable_pct", "co2_g_per_kwh", "frequency_hz", "grid_status",
        ),
    ),
    DataTypeSpec(
        "Vehicle Trip",
        generate_trip,
        (
            "trip_id", "vehicle_id", "vehicle_type", "distance_km",
            "duration_min", "avg_speed_kmh", "energy_kwh", "regen_kwh", "co2_saved_kg", "route",
        ),
    ),
)

DATA_TYPE_LABELS: tuple[str, ...] = tuple(spec.label for spec in DATA_TYPES)
DATA_TYPE_MAP: dict[str, DataTypeSpec] = {spec.label: spec for spec in DATA_TYPES}


def normalize_record(record: Record, columns: tuple[str, ...]) -> Record:
    """Keep only the fields that belong to the active data type."""
    return {column: record[column] for column in columns}


def parse_field_value(raw: str, original: object) -> object:
    """Coerce manual-entry text to the same type as the original value."""
    value = raw.strip()
    if not value or value == str(original):
        return original
    if isinstance(original, bool):
        return value.lower() in {"1", "true", "yes"}
    if isinstance(original, int):
        try:
            return int(value)
        except ValueError:
            return value
    if isinstance(original, float):
        try:
            return float(value)
        except ValueError:
            return value
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def table_name_from_label(label: str) -> str:
    """Convert a data-type label into a safe SQL table name."""
    name = label.lower().replace(" & ", "_").replace(" ", "_").replace("-", "_")
    return "".join(char for char in name if char.isalnum() or char == "_")


def sql_literal(value: object) -> str:
    """Format a Python value as an SQL literal."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def infer_sql_type(value: object) -> str:
    """Infer a portable SQL column type from a sample value."""
    if isinstance(value, bool):
        return "INTEGER"
    if isinstance(value, int):
        return "INTEGER"
    if isinstance(value, float):
        return "REAL"
    return "TEXT"


def infer_column_types(records: list[Record], columns: tuple[str, ...]) -> dict[str, str]:
    """Infer SQL types across all records for consistent schemas."""
    column_types = {column: infer_sql_type(records[0][column]) for column in columns}
    for record in records[1:]:
        for column in columns:
            if column_types[column] == "TEXT" and isinstance(record[column], (int, float)):
                column_types[column] = infer_sql_type(record[column])
    return column_types


def build_sql_script(table_name: str, records: list[Record], columns: tuple[str, ...]) -> str:
    """Build a SQL script with CREATE TABLE and INSERT statements."""
    column_types = infer_column_types(records, columns)

    column_defs = ",\n    ".join(
        f"{column} {column_types[column]}" for column in columns
    )
    lines = [
        "-- EMDT Test Data Generator",
        f"-- Table: {table_name}",
        f"-- Records: {len(records)}",
        "",
        f"CREATE TABLE IF NOT EXISTS {table_name} (",
        f"    {column_defs}",
        ");",
        "",
    ]

    for record in records:
        values = ", ".join(sql_literal(record[column]) for column in columns)
        column_list = ", ".join(columns)
        lines.append(f"INSERT INTO {table_name} ({column_list}) VALUES ({values});")

    lines.append("")
    return "\n".join(lines)


def write_sqlite_database(
    path: Path, table_name: str, records: list[Record], columns: tuple[str, ...]
) -> None:
    """Write records into a SQLite database file."""
    if path.exists():
        path.unlink()

    column_types = infer_column_types(records, columns)
    column_defs = ", ".join(f"{column} {column_types[column]}" for column in columns)

    with sqlite3.connect(path) as connection:
        connection.execute(f"CREATE TABLE {table_name} ({column_defs})")
        placeholders = ", ".join("?" for _ in columns)
        column_list = ", ".join(columns)
        connection.executemany(
            f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})",
            [[record[column] for column in columns] for record in records],
        )
        connection.commit()


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

class EMDTApp:
    """Desktop UI for generating and exporting EMDT test datasets."""

    def __init__(self, theme: Theme = THEME) -> None:
        self.theme = theme
        self.generated_data: list[Record] = []
        self.active_spec: DataTypeSpec | None = None
        self._banner_image: ImageTk.PhotoImage | None = None

        self.root = tk.Tk()
        self.root.title("EMDT Data Generator")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=theme.bg)
        self.root.resizable(True, True)

        self.status_var = tk.StringVar(
            value="Ready — select a data type and click Generate or Manual."
        )

        self._configure_styles()
        self._build_banner()
        self._build_controls()
        self._build_status_bar()
        self._build_table()
        self._build_footer()

    def run(self) -> None:
        self.root.mainloop()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        t = self.theme
        style.configure(
            "TCombobox",
            fieldbackground=t.card,
            background=t.card,
            foreground=t.text,
            selectbackground=t.accent,
            bordercolor=t.border,
            arrowcolor=t.text,
        )
        style.configure(
            "Treeview",
            background=t.card,
            foreground=t.text,
            fieldbackground=t.card,
            rowheight=26,
            bordercolor=t.border,
        )
        style.configure(
            "Treeview.Heading",
            background=t.accent_secondary,
            foreground=t.text,
            font=t.font_small + ("bold",),
        )
        style.map("Treeview", background=[("selected", t.accent_secondary)])
        style.configure(
            "Vertical.TScrollbar",
            background=t.card,
            troughcolor=t.panel,
            arrowcolor=t.accent,
        )

    def _build_banner(self) -> None:
        t = self.theme
        banner_path = find_banner_path()

        if banner_path:
            try:
                image = Image.open(banner_path).resize(BANNER_SIZE, Image.LANCZOS)
                self._banner_image = ImageTk.PhotoImage(image)
                tk.Label(self.root, image=self._banner_image, bg=t.bg).pack(fill="x")
                return
            except OSError as error:
                self.status_var.set(f"Banner image found but could not be loaded: {error}")

        tk.Label(
            self.root,
            text="EMDT — Electric Mobility Digital Twin — Test Data Generator",
            bg=t.accent_secondary,
            fg=t.text,
            font=(t.font_family, t.font_size_banner, "bold"),
            pady=18,
        ).pack(fill="x")

    def _build_controls(self) -> None:
        t = self.theme
        controls = tk.Frame(self.root, bg=t.panel, pady=10)
        controls.pack(fill="x")

        tk.Label(controls, text="Data Type:", bg=t.panel, fg=t.text, font=t.font).grid(
            row=0, column=0, padx=(20, 6)
        )

        self.data_type_combo = ttk.Combobox(
            controls, width=22, state="readonly", font=t.font, values=DATA_TYPE_LABELS
        )
        self.data_type_combo.current(0)
        self.data_type_combo.grid(row=0, column=1, padx=(0, 20))
        self.data_type_combo.bind("<<ComboboxSelected>>", self._on_data_type_changed)

        tk.Label(controls, text="Records:", bg=t.panel, fg=t.text, font=t.font).grid(
            row=0, column=2, padx=(0, 6)
        )

        self.record_count_spinbox = tk.Spinbox(
            controls,
            from_=MIN_RECORDS,
            to=MAX_RECORDS,
            width=6,
            bg=t.card,
            fg=t.text,
            insertbackground=t.text,
            buttonbackground=t.accent_secondary,
            font=t.font,
            relief="flat",
        )
        self.record_count_spinbox.delete(0, tk.END)
        self.record_count_spinbox.insert(0, "10")
        self.record_count_spinbox.grid(row=0, column=3, padx=(0, 20))

        buttons = (
            ("Generate", t.accent, self.generate_records, 4),
            ("Manual", t.accent_secondary, self.open_manual_entry, 5),
            ("Clear", t.red, self.clear_records, 6),
            ("CSV", t.green, self.export_csv, 7),
            ("JSON", t.purple, self.export_json, 8),
            ("SQL", t.orange, self.export_sql, 9),
        )
        for text, color, command, column in buttons:
            self._make_button(controls, text, color, command, column)

    def _make_button(
        self, parent: tk.Frame, text: str, color: str, command: object, column: int
    ) -> tk.Button:
        t = self.theme
        button = tk.Button(
            parent,
            text=text,
            bg=color,
            fg=t.bg,
            activebackground=t.btn_hover,
            activeforeground=t.text,
            font=t.font_bold,
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=command,
        )
        button.grid(row=0, column=column, padx=6)
        return button

    def _build_status_bar(self) -> None:
        t = self.theme
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=t.card,
            fg=t.muted,
            font=t.font_small,
            anchor="w",
            padx=16,
            pady=5,
        ).pack(fill="x")

    def _build_table(self) -> None:
        t = self.theme
        table_frame = tk.Frame(self.root, bg=t.bg)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(6, 0))

        self.tree = ttk.Treeview(table_frame, show="headings", selectmode="browse")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def _build_footer(self) -> None:
        t = self.theme
        tk.Label(
            self.root,
            text="EMDT-TDG  •  LAB University of Applied Sciences  •  Yeganeh Maleki  •  2026",
            bg=t.panel,
            fg=t.muted,
            font=(t.font_family, 8),
            pady=6,
        ).pack(fill="x", side="bottom")

    def _on_data_type_changed(self, _event: object = None) -> None:
        """Clear stale data when the user picks a different data type."""
        if not self.generated_data or not self.active_spec:
            return

        new_label = self.data_type_combo.get()
        if new_label == self.active_spec.label:
            return

        if messagebox.askyesno(
            "Change Data Type",
            "Switching data type will clear the current table. Continue?",
        ):
            self.clear_records()
        else:
            self.data_type_combo.set(self.active_spec.label)

    def _selected_spec(self) -> DataTypeSpec:
        return DATA_TYPE_MAP[self.data_type_combo.get()]

    def _read_record_count(self) -> int | None:
        try:
            count = int(self.record_count_spinbox.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Record count must be a whole number.")
            return None
        if not MIN_RECORDS <= count <= MAX_RECORDS:
            messagebox.showerror(
                "Invalid Input",
                f"Record count must be between {MIN_RECORDS} and {MAX_RECORDS}.",
            )
            return None
        return count

    def _configure_tree_columns(self, columns: tuple[str, ...]) -> None:
        self.tree["columns"] = columns
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(
                column, width=COLUMN_WIDTH, anchor="center", minwidth=COLUMN_MIN_WIDTH
            )

    def _populate_tree(self, records: list[Record], columns: tuple[str, ...]) -> None:
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", values=[record[col] for col in columns])

    def generate_records(self) -> None:
        count = self._read_record_count()
        if count is None:
            return

        spec = self._selected_spec()
        self.active_spec = spec
        self._configure_tree_columns(spec.columns)
        self.generated_data = [
            normalize_record(spec.generator(), spec.columns) for _ in range(count)
        ]
        self._populate_tree(self.generated_data, spec.columns)

        self.status_var.set(
            f"{count} records generated | Type: {spec.label} | "
            f"Columns: {len(spec.columns)} | Ready to export."
        )

    def clear_records(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self.generated_data.clear()
        self.active_spec = None
        self.status_var.set("Cleared.")

    def open_manual_entry(self) -> None:
        spec = self._selected_spec()
        if self.active_spec and self.active_spec.label != spec.label:
            messagebox.showwarning(
                "Data Type Mismatch",
                f"The table contains {self.active_spec.label} data.\n"
                f"Clear the table or switch back before adding {spec.label} records.",
            )
            return
        ManualEntryDialog(self, spec)

    def add_manual_record(self, record: Record, spec: DataTypeSpec) -> None:
        if self.active_spec and self.active_spec.label != spec.label:
            messagebox.showerror(
                "Data Type Mismatch",
                "This record does not match the data currently in the table.",
            )
            return

        record = normalize_record(record, spec.columns)

        if not self.tree["columns"]:
            self._configure_tree_columns(spec.columns)
            self.active_spec = spec

        self.generated_data.append(record)
        self.tree.insert("", "end", values=[record[col] for col in spec.columns])
        self.status_var.set(f"Manual entry added | Total records: {len(self.generated_data)}")

    def _export_records(self) -> list[Record] | None:
        if not self._ensure_data_present() or not self.active_spec:
            return None
        return self.generated_data

    def export_csv(self) -> None:
        records = self._export_records()
        if records is None or not self.active_spec:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save as CSV",
        )
        if not path:
            return

        columns = self.active_spec.columns
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                writer.writerows(records)
        except OSError as error:
            messagebox.showerror("Export Failed", f"Could not save CSV file:\n{error}")
            return

        messagebox.showinfo("Saved", f"CSV file saved:\n{path}")
        self.status_var.set(f"CSV exported → {path}")

    def export_json(self) -> None:
        records = self._export_records()
        if records is None:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save as JSON",
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(records, handle, ensure_ascii=False, indent=2)
        except OSError as error:
            messagebox.showerror("Export Failed", f"Could not save JSON file:\n{error}")
            return

        messagebox.showinfo("Saved", f"JSON file saved:\n{path}")
        self.status_var.set(f"JSON exported → {path}")

    def export_sql(self) -> None:
        records = self._export_records()
        if records is None or not self.active_spec:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[
                ("SQL script", "*.sql"),
                ("SQLite database", "*.db"),
            ],
            title="Save as SQL",
        )
        if not path:
            return

        table_name = table_name_from_label(self.active_spec.label)
        columns = self.active_spec.columns
        file_path = Path(path)

        try:
            if file_path.suffix.lower() == ".db":
                write_sqlite_database(file_path, table_name, records, columns)
            else:
                sql_script = build_sql_script(table_name, records, columns)
                file_path.write_text(sql_script, encoding="utf-8")
        except (OSError, sqlite3.Error) as error:
            messagebox.showerror("Export Failed", f"Could not save SQL file:\n{error}")
            return

        messagebox.showinfo("Saved", f"SQL file saved:\n{path}")
        self.status_var.set(f"SQL exported → {path}")

    def _ensure_data_present(self) -> bool:
        if self.generated_data:
            return True
        messagebox.showwarning("No Data", "Please generate data first.")
        return False


class ManualEntryDialog:
    """Modal form for adding a single record by hand."""

    def __init__(self, app: EMDTApp, spec: DataTypeSpec) -> None:
        self.app = app
        self.spec = spec
        t = app.theme

        self.window = tk.Toplevel(app.root)
        self.window.title(f"Add Manual Entry — {spec.label}")
        self.window.geometry("400x500")
        self.window.configure(bg=t.bg)
        self.window.resizable(False, False)
        self.window.transient(app.root)
        self.window.grab_set()

        if (
            app.active_spec
            and app.active_spec.label == spec.label
            and app.generated_data
        ):
            self.base_row = app.generated_data[-1].copy()
            help_text = "Previous row values are loaded. Edit fields or leave unchanged."
        else:
            self.base_row = normalize_record(spec.generator(), spec.columns)
            help_text = "Sample values are loaded. Edit fields or leave unchanged."

        tk.Label(
            self.window,
            text=f"Manual Entry — {spec.label}",
            bg=t.bg,
            fg=t.accent,
            font=t.font_title,
        ).pack(pady=(20, 10))

        tk.Label(self.window, text=help_text, bg=t.bg, fg=t.muted, font=t.font_small).pack(
            pady=(0, 16)
        )

        frame = tk.Frame(self.window, bg=t.bg)
        frame.pack(fill="both", expand=True, padx=30)

        self.entries: dict[str, tk.Entry] = {}
        for index, column in enumerate(spec.columns):
            tk.Label(frame, text=f"{column}:", bg=t.bg, fg=t.text, font=t.font_small).grid(
                row=index, column=0, sticky="w", pady=4
            )
            entry = tk.Entry(
                frame,
                width=25,
                bg=t.card,
                fg=t.text,
                insertbackground=t.accent,
                font=t.font_small,
                relief="flat",
            )
            entry.grid(row=index, column=1, padx=(10, 0), pady=4, ipady=4)
            entry.insert(0, str(self.base_row.get(column, "")))
            self.entries[column] = entry

        tk.Button(
            self.window,
            text="Add to Table",
            bg=t.green,
            fg=t.bg,
            activebackground=t.btn_hover,
            font=t.font_bold,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.submit,
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Cancel",
            bg=t.card,
            fg=t.red,
            font=t.font_small,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.window.destroy,
        ).pack()

    def submit(self) -> None:
        row = self.base_row.copy()
        for column, entry in self.entries.items():
            row[column] = parse_field_value(entry.get(), row[column])

        row = normalize_record(row, self.spec.columns)
        self.app.add_manual_record(row, self.spec)
        self.window.destroy()


def main() -> None:
    EMDTApp().run()


if __name__ == "__main__":
    main()
