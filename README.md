
# EMDT Test Data Generator: Change Report

**Version:** 2.5.0  
**Date:** 11 October 2026  
**Author:** Yeganeh Maleki, LAB University of Applied Sciences

## Summary

The record limit per run was raised from 1,000 to 10,000, and the map was changed so it stays responsive at that size. A second round fixed data-quality and input problems found while reviewing the code: duplicate IDs, inconsistent trip durations, charging locations that did not match their GPS position, unchecked `nan`/`inf` input, and hard-to-read statistics. A README was added. All changes are in one Python file plus the README.

## Changes

### Capacity and performance

**C1. Record limit raised.** 1,000 → 10,000 records per run. The Records spinbox and the input check both read this one setting, so nothing else needed to change.
Code: `AppConfig.max_records`

**C2. Map draws a sample of large datasets.** The map redraws every point on each zoom or pan, which would be slow with 10,000 records. It now draws every n-th record, about 2,000 to 4,000 points. The table, statistics and all exports still contain every record, and the map header still shows the true total.
Code: `MapPanel._render`, `draw_records`

### Data quality

**C3. Unique, sequential IDs.** Session and trip IDs were random four-digit numbers (only 9,000 possible values), so duplicates were certain at 10,000 records. They are now sequential (`CHG-0001`, `TRIP-0001`, `KMP-00001`). Counters restart at each Generate, so the same seed gives the same IDs.
Code: `_next_id`, `_reset_id_counters`, `generate_charging_session`, `generate_trip`, `generate_kempower_session`

**C4. Trip duration follows distance and speed.** Duration was an independent random number (e.g. 600 km in 5 minutes). It is now calculated as distance ÷ average speed.
Code: `generate_trip`

**C5. Charging location matches GPS.** "Lahti Supercharger" and "Helsinki Supercharger" rows now sit within about 1 km of those cities. Before, their coordinates came from anywhere in Finland. "Home Charger" and "Shopping Mall" still use a random position.
Code: `_CHARGING_LOCATIONS`, `generate_charging_session`

### Input and display

**C6. Manual entry rejects `nan` and `inf`.** `nan` passed validation because every comparison with it is false, and `inf` passed fields without a maximum. Both now raise a clear error.
Code: `parse_field_value`

**C7. Manual entry assigns a new ID.** The form is pre-filled from the last row, so saving it unchanged created a duplicate ID. The session or trip ID is now increased to the next free number.
Code: `_next_unique_id`, `ManualEntryDialog`

**C8. Readable statistics.** Values such as 150000 were shown as `1.5e+05` and 45.3 as `45`. They now appear as `150,000` and `45.3`.
Code: `_fmt_stat`, `StatsPanel.update`

### Maintenance and documentation

**C9. Version strings, comments, unused code.** The file header said v2.1, the version constant said 2.5.0 and the SQL header said v2; all now follow `__version__`. The manual-entry dialog is described as non-modal (as it is). A misleading map comment was corrected and an unused variable removed.

**C10. README added.** Requirements, how to run, usage, data types, configuration, limitations and roadmap, formatted for GitHub.

## Verification

Checks ran without a display, with Tkinter replaced by a stub. The application window itself was not opened.

- Checked: the file compiles without syntax errors.
- Checked: 10,000 records each of Charging Session, Vehicle Trip and Kempower Station Session had all-unique IDs (C3).
- Checked: 5,000 generated trips had duration equal to distance ÷ speed in every case (C4).
- Checked: all 2,540 generated Lahti and Helsinki charging rows lay within 3 km of their named city (C5).
- Checked: `nan`, `inf` and `-inf` were rejected and a normal number such as 12.5 was accepted (C6).
- Checked: the manual-entry form logic gave a new, non-colliding ID for charging sessions and trips (C7), and statistics formatting gave the expected text for sample values (C8).
- Checked: 10,000 generated records of each of the six data types broke no field rule (measured before round two; Charging Session re-checked after C5). Generating 10,000 records took 70 to 200 ms.
- **Not yet checked:** running the full window with 10,000 records (table fill time, map zoom and pan, CSV/JSON/SQL/SQLite export dialogs, layout on the presentation laptop).

## Known limitations

- The data is synthetic. Most fields are random and independent, and records do not form a continuous time series for one vehicle.
- Charging energy is not derived from the change in state of charge. In a 5,000-row sample, about 40% of rows differ from the SOC-implied energy by more than 20 kWh.
- About 15% of generated trips (745 of 5,000) need more energy than the largest battery in the generator (82 kWh).
- Random GPS points come from a rectangle around Finland, so some fall at sea or in neighbouring countries.
- A seed does not fix `timestamp`, which is taken from the current time.
- Filling the table with 10,000 rows may freeze the window for a moment. Generation runs on a background thread, but the table, statistics and map are updated on the main thread afterwards.
- Export and Delete Row stay enabled during generation, and a failed generation can leave the table half updated.
- Kempower station details and vehicle specifications are approximate and not checked against official sources.
- There are no automated tests yet.

## Suggested next steps

- Derive charging energy from SOC and battery capacity, and keep trip energy within battery capacity.
- Generate per-vehicle time series with continuously changing SOC, speed and position.
- Import real GPS tracks (GPX) and vehicle data (OBD-II or a vehicle API).
- Insert table rows in chunks and lock the export buttons during generation.
- Add unit tests for the validators and generators, and a command-line mode without the window.

**Files changed:** `emdt_test_data_generator.py`  
**Files added:** `README.md`
```

این متن Markdown است و در GitHub، Notion یا Word (با paste) خوب نمایش داده می‌شود. اگر برای ایمیل متن ساده (بدون علامت‌های `#` و `**`) می‌خواهی، بگو تا همان را بدون فرمت بدهم.
