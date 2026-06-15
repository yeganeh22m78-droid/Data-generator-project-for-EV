🚗 EMDT Test Data Generator (EMDT‑TDG)
Synthetic Electric Vehicle Data Generator for the Electric Mobility Digital Twin Project
A desktop application built with Python, Tkinter, and SQLite for generating realistic synthetic EV datasets.
Designed for the Electric Mobility Digital Twin (EMDT) project at LAB University of Applied Sciences.

📌 Features
🔋 Five EV Data Categories
Battery Sensor Data

Charging Session Data

Powertrain & Motor Data

Grid & Energy Mix Data

Trip & Driving Telemetry

🖥️ Modern Desktop UI
Custom dark theme

Banner image (Pillow)

Dynamic table (Treeview)

Status bar + footer

Manual entry dialog

📤 Export Formats
CSV

JSON

SQL script (CREATE TABLE + INSERT)

SQLite database (.db)

🧠 Smart Data Handling
SQL type inference

Data normalization

Type‑safe manual entry

Linked UI components

Realistic EV values based on Tesla Model 3 specifications

🛠️ Technologies Used
Python 3.12

Tkinter (GUI)

Pillow (image handling)

SQLite3

CSV / JSON

Dataclasses & Type Hints

🚀 How to Run
bash
python main.py
No installation required — all dependencies except Pillow are built into Python.

Install Pillow if needed:

bash
pip install pillow
📂 Project Structure
Code
EMDT-TDG/
 ├── main.py
 ├── theme.py
 ├── data_generators.py
 ├── export_sql.py
 ├── manual_entry.py
 ├── assets/
 │    └── ev_banner.png
 └── README.md
📸 Screenshots
(Add your own screenshots here)

Code
[ UI Screenshot ]
[ Manual Entry Dialog ]
[ Export Examples ]
📊 Data Types Overview
🔋 Battery Sensor Data
SOC (%)

Voltage (V)

Current (A)

Temperature (°C)

Health (%)

Charge cycles

Status (Charging / Driving / Idle)

⚡ Charging Session
Charger type (AC / DC)

Start & end SOC

Energy delivered (kWh)

Duration (min)

Cost (€)

🏎️ Powertrain & Motor
Speed (km/h)

Motor RPM (0–19,000)

Torque (Nm)

Motor & inverter temperature

Efficiency (%)

🌍 Grid & Energy Mix
Solar & wind power (kW)

Grid load (kW)

EV load (kW)

Renewable %

CO₂ intensity (g/kWh)

Frequency (Hz)

🚘 Trip & Driving
Distance (km)

Duration (min)

Avg speed (km/h)

Energy consumption (kWh)

Regenerative braking (kWh)

CO₂ saved (kg)

🧪 Why These Values Are Realistic
All ranges and values are based on real Tesla Model 3 specifications and EV research sources.

Primary Source (Official):
Tesla Model 3 — https://www.tesla.com/model3

Additional Technical Sources:
TopSpeed — Battery size, voltage, charging

Recurrent Auto — Battery behavior

LamMotor — Motor RPM & torque

EVSpecifications — Full technical specs

Tesla Owner’s Manual — Temperature & charging limits

FleetNews — Long Range model data

🧩 Project Purpose
This tool was developed for the Electric Mobility Digital Twin (EMDT) project to provide:

High‑quality synthetic EV datasets

For simulation, testing, and research

When real EV hardware data is unavailable

👩‍💻 Author
Yeganeh Maleki  
LAB University of Applied Sciences
2026
