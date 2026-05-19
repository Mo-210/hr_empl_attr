# HR Employee Attrition

**[Live dashboard](https://hremplattr-irq6o2otusuc9f79adb7sc.streamlit.app/)** — filters work in the browser, nothing to install.

I built this to practice HR analytics on a familiar dataset (~1,470 employee records). I started in a Jupyter notebook, wrote up the main takeaways in a PDF, then put the charts into a Streamlit app so I could click through departments and roles without re-running cells.

## What stood out

- Overall attrition is **16.1%** (237 people left).
- **Sales** has the highest department rate (**20.6%**), not R&D.
- **Sales Representative** is almost **40%** — that was the number that made me dig deeper into role-level views.
- Most people who left had **low job satisfaction**; tenure and age patterns point to early- and mid-career risk more than long-tenured staff.

More detail in `reports/employee_attrition_recommendations.pdf`.

## Run locally

```bash
python run.py
```

On Windows: `scripts\run_dashboard.bat` also works.

Main pieces: `data/` (Excel file), `notebooks/attrition_analysis.ipynb` (EDA walkthrough), `app/dashboard.py`, shared helpers in `src/`.

## Tech

pandas, Plotly, Streamlit, matplotlib/seaborn in the notebook.

## Data

Public HR attrition dataset; I first saw a version on [Abdalluh2024's repo](https://github.com/Abdalluh2024). The analysis, dashboard, and write-up here are my own.
