# ⚡ EMDT Test Data Generator

A desktop application for generating realistic test data for the **Electric Mobility Digital Twin (EMDT)** project — a research initiative by LAB University of Applied Sciences and LUT University, funded by the European Union (EAKR).

---

## 📌 About This Project

This tool was built as part of a first-year IT internship at LAB University of Applied Sciences (Lahti, Finland). The goal is to generate realistic fake data for testing the EMDT platform — a modular digital twin architecture for electric mobility systems.

The generated data simulates real-world electric vehicle (EV) sensor readings, enabling developers to test the platform without needing actual vehicle hardware.

---

## 🚗 Data Types

The generator produces five types of EV-related test data:

| Data Type | Fields |
|---|---|
| **Battery Sensor** | State of charge, voltage, temperature, current, health |
| **Charging Session** | Charger type, location, energy delivered, cost, duration |
| **Powertrain & Motor** | Speed, RPM, torque, motor efficiency, temperatures |
| **Grid & Energy** | Solar/wind power, grid load, CO₂ intensity |
| **Vehicle Trip** | Distance, energy used, CO₂ saved, route type |

---

## 🛠 Built With

- **Python** — core language
- **Tkinter** — desktop UI (built-in, no installation needed)
- **random** — realistic data generation (built-in)
- **json** — JSON export (built-in)
- **csv** — CSV export (built-in)

> No external libraries required. Everything runs on standard Python.

---

## 🚀 Getting Started

### Requirements

- Python 3.x

### Run

```bash
python emdt_data_generator.py
```

No `pip install` needed.

---

## 🖥 How to Use

1. Select a **data type** from the dropdown (Battery, Charging, Powertrain, Grid, Trip)
2. Choose the **number of records** to generate (1–1000)
3. Click **Generate** — data appears in the table instantly
4. Export as **CSV** (Excel-compatible) or **JSON** (developer-friendly)

---

## 📁 Output Formats

| Format | Best For |
|---|---|
| **CSV** | Non-technical stakeholders, Excel users |
| **JSON** | Developers, API testing, system integration |

Both formats were chosen to serve the two main user groups identified in the EMDT project documentation: engineers who need structured data for APIs, and non-technical stakeholders who prefer spreadsheets.

---

## 🔬 About the EMDT Project

The **Electric Mobility Digital Twin** project aims to create a modular, scalable digital twin platform architecture that supports the comprehensive development of electric mobility. It is implemented as a group project between:

- **LAB University of Applied Sciences** — software and data architecture
- **LUT University (EMRC)** — electric mobility research and hardware expertise

The project is co-funded by the European Union through the European Regional Development Fund (EAKR), under the programme *Uudistuva ja osaava Suomi 2021–2027*.

---

## 📚 References & Inspiration

- [EMDT Project Documentation (EAKR 2021/406132)](https://www.eura2021.fi)
- [Faker Library](https://faker.readthedocs.io) — studied for data generation patterns
- [InfluxDB EV Data Generator](https://github.com) — studied for EV field structure
- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

## 👤 Author

**Yeganeh Maleki**
First-year IT student — LAB University of Applied Sciences
Internship project, 2025–2026

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
