## 🛠 Project Setup

### Environment Setup

This project was developed using **Visual Studio Code (VS Code)** with a Python virtual environment. To replicate the environment:

1. **Create a virtual environment**:

```bash
python -m venv my_env1
```

2. **Activate the virtual environment**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\my_env1\Scripts\Activate.ps1
```

3. **Install required packages**:

```bash
pip install numpy pandas seaborn matplotlib plotly openpyxl
```

## 🧠 Analysis Overview

The project leverages structured HR data to explore the dynamics of employee attrition. It includes:

- Department-wise and role-wise attrition analysis
- Attrition breakdown by education field, job satisfaction, salary tier, and more
- Percentage-based annotations for clarity
- Use of both bar charts and donut charts for visual storytelling

## 📊 Libraries Used

- **pandas** – Data manipulation
- **matplotlib / seaborn** – Static data visualization
- **plotly** – Interactive visualizations (optional enhancement)
- **openpyxl** – Excel support

## 📁 Structure

- `*.py` files: Contain modular visualization and analysis scripts
- `data/`: Raw HR dataset
- `notebooks/`: Optional Jupyter exploration (if any)
- `charts/`: Generated plots for reporting or presentation

## ✅ Current Status

- Cleaned and processed dataset
- Executed exploratory visualizations for categorical and numerical features
- Set up for possible extension into predictive modeling or dashboards

## 🚀 Future Plans

- Integrate with Streamlit or Dash for interactive dashboards
- Add predictive modeling to classify attrition risk
- Expand analysis to team-level and manager-level insights

---

This project is based on a public HR analytics repository originally created by Abdalluh2024 on GitHub. While the initial dataset and project structure were sourced from that work, the analysis, visualizations, and enhancements presented here are original contributions developed independently.

