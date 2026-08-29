# EMDT Test Data Generator

**Electric Mobility Digital Twin — Test Data Generator (v2.5)**

A desktop application built with Python and Tkinter that generates realistic, configurable test data for electric vehicle digital twin systems — including battery sensors, charging sessions, powertrain telemetry, grid/energy data, vehicle trips, and real-world Kempower charging station sessions.

---

## 📌 Overview

Teams developing digital twin systems for electric vehicles need realistic sample data to test their software before real hardware or field data is available. **EMDT Test Data Generator** solves this by producing physically realistic, reproducible test data across six sensor/event types, with built-in validation, visualization, and multiple export formats.

## ✨ Features

- **Six data types**: Battery Sensor, Charging Session, Powertrain & Motor, Grid & Energy, Vehicle Trip, and Kempower Station Session (using real GPS coordinates from 12 actual charging stations in Finland).
- **Realistic value ranges**: e.g. vehicle speed based on real Tesla Model 3 specifications, GPS coordinates constrained to Finland's borders.
- **Reproducible data**: generate the exact same dataset again using a seed value — useful for repeatable QA testing.
- **Responsive UI**: data generation runs on a background thread (via Python's `threading` and `queue` modules) so the interface never freezes, even with large record counts.
- **Data validation**: every field is checked against defined ranges or allowed values, including cross-field rules (e.g. charge percentage must increase over a session).
- **Interactive map**: view generated GPS data (points or trips) on a simple, offline schematic map with pan, zoom, and category-based coloring.
- **Manual entry**: add or edit individual records by hand, with the same validation rules applied.
- **Multiple export formats**: CSV, JSON, SQL script, or a ready-to-use SQLite database file.

## 🖥️ Screenshot

*(Add a screenshot of the running application here)*

## 🛠️ Built With

- **Python 3** — core language
- **Tkinter** — graphical user interface
- **threading / queue** — background data generation without freezing the UI
- **sqlite3** — SQLite database export
- **Pillow (optional)** — banner image support (app works without it)
- **logging** — console and file logging (`emdt.log`)

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- (Optional) [Pillow](https://pypi.org/project/pillow/) for the banner image:
  ```bash
  pip install pillow
  ```

### Running the app

```bash
python emdt_test_data_generator_v2.5_advanced_map.py
```

## 📖 Usage

1. Select a data type from the dropdown (e.g. *Battery Sensor*).
2. Set the number of records, the time interval between them, and (optionally) a seed for reproducible results.
3. Click **Generate**.
4. View the data in the table, check summary statistics, or view GPS data on the map.
5. Export the data using the **CSV**, **JSON**, **SQL**, or **SQLite** buttons.

## 🏗️ Architecture Notes

- Each data type is defined by a small generator function and registered in a central `DATA_TYPES` registry — adding a new sensor type only requires writing one function and one registry entry.
- Data generation and validation logic are fully decoupled from the UI, making them independently testable.
- All configuration values (window size, record limits, colors, fonts) are centralized in `AppConfig` and `Theme` dataclasses rather than scattered through the code.

## ⚠️ Limitations

- Currently implemented as a single file; a larger version of this project would benefit from being split into separate modules (generators, UI, export).
- No automated test suite yet — the generator and validation functions are pure functions and would be straightforward to test with `pytest`.
- The map is a simplified schematic for visual orientation only, not an accurate geographic projection.

## 👤 Author

**Yeganeh Maleki**
First-Year IT Student, LAB University of Applied Sciences

## 📄 License

*(Add a license here, e.g. MIT, if you'd like others to be able to reuse this code)*
