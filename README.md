# RTA Dashboard — Data Storytelling Project

Brief Description

- Project: Road Traffic Accident (RTA) Visualization & Data Storytelling Dashboard
- Author: Kangmin Yu (kangmin.yu@efrei.net)
- Supervisor: Mano Joseph Mathew (mano.mathew@efrei.fr)
- Objective: Clean, analyze, and present RTA data through an interactive dashboard to support decision-making and intervention recommendations.

Quick Start

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the application:

```powershell
streamlit run app.py
```

Key Files

- `app.py` — Main application file, including page layout, sidebar, and section displays (KPIs, geographic/temporal/factor analysis, data quality, insights).
- `Chinese.py` — Chinese version example (can be run directly instead of app.py).
- `utils/` — Utility modules (io.py, prep.py, viz.py) for data loading & preprocessing, unified visualization functions, etc.
- `sections/` — Modular sections to split the page (e.g., intro.py, overview.py, deep_dives.py, conclusions.py).
- `requirements.txt` — Recommended dependency list.
- `RTA Dataset.csv` — Raw data file (should be placed in the project root directory; modify DATA_PATH if the filename differs).

Notes

- If the dataset is large, some real-time visualizations may be slow. It is recommended to preprocess the data and save it to data/processed.parquet to improve loading speed.
- The "Data Quality" module in app.py lists missing values and duplicate rows. Prioritize handling fields with severe missing data before relying on them for critical decisions.
- When deploying to Streamlit Community Cloud or other platforms, ensure data access settings (private/public) and dependency installation are configured in the deployment settings.

Contact Information

- Author:kangmin.yu@efrei.net
- Supervisor:mano.mathew@efrei.fr

---