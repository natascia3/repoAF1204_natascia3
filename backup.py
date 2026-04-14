# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.22.4",
#     "pandas>=3.0.2",
#     "plotly>=6.6.0",
#     "uv>=0.11.6",
# ]
# ///

import marimo

__generated_with = "0.23.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px


@app.cell
def _(mo, pd):
    path_to_csv = mo.notebook_location() / "public" / "sp500_ZScore_AvgCostofDebt.csv"
    df = pd.read_csv(str(path_to_csv))
    df = df.dropna(subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key", "Market_Cap"])
    df = df[df["AvgCost_of_Debt"] < 0.15].copy()

    df["Debt_Cost_Percent"] = df["AvgCost_of_Debt"] * 100
    df["Market_Cap_B"] = df["Market_Cap"] / 1e9

    return (df,)


@app.cell
def _(df, mo):
    sectors = sorted(df["Sector_Key"].unique().tolist())

    sector_dropdown = mo.ui.multiselect(
        options=sectors,
        value=sectors[:4],
        label="Filter by Sector",
    )

    cap_slider = mo.ui.slider(
        start=0,
        stop=200,
        step=10,
        value=0,
        label="Min Market Cap ($ Billions)",
    )

    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df, sector_dropdown):
    filtered = df[
        (df["Sector_Key"].isin(sector_dropdown.value))
        & (df["Market_Cap_B"] >= cap_slider.value)
    ].copy()

    return (filtered,)


@app.cell
def _(filtered, mo, px):
    fig = px.scatter(
        filtered,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        size="Market_Cap_B",
        hover_name="Name",
        title="Cost of Debt vs Credit Risk",
        labels={
            "Z_Score_lag": "Altman Z-Score",
            "Debt_Cost_Percent": "Cost of Debt (%)",
            "Sector_Key": "Sector",
            "Market_Cap_B": "Market Cap ($B)",
        },
        template="presentation",
        width=900,
        height=600,
    )

    fig.add_vline(x=1.81, line_dash="dash", line_color="red")
    fig.add_vline(x=2.99, line_dash="dash", line_color="green")

    scatter_chart = mo.ui.plotly(fig)
    return (scatter_chart,)


@app.cell
def _(filtered, mo, px):
    hist_fig = px.histogram(
        filtered,
        x="Z_Score_lag",
        color="Sector_Key",
        nbins=25,
        title="Distribution of Altman Z-Scores",
        labels={
            "Z_Score_lag": "Altman Z-Score",
            "Sector_Key": "Sector",
        },
        template="presentation",
        width=900,
        height=500,
        barmode="overlay",
        opacity=0.75,
    )

    hist_chart = mo.ui.plotly(hist_fig)
    return (hist_chart,)


@app.cell
def _(filtered, mo, px):
    box_fig = px.box(
        filtered,
        x="Sector_Key",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        title="Cost of Debt by Sector",
        labels={
            "Sector_Key": "Sector",
            "Debt_Cost_Percent": "Cost of Debt (%)",
        },
        template="presentation",
        width=900,
        height=550,
        points="outliers",
    )

    box_fig.update_layout(xaxis_tickangle=-35)

    box_chart = mo.ui.plotly(box_fig)
    return (box_chart,)


@app.cell
def _(mo):
    tab_cv = mo.md("""
### Natascia Hossain  
**BSc Accounting & Finance Student | Aspiring Financial Analyst**

---

### Professional Profile
I am a BSc Accounting and Finance student at Bayes Business School with a strong interest in financial analysis, Python, marimo, and data visualisation. I enjoy using data tools to explore real-world business problems and communicate insights clearly.

I have developed strong adaptability, communication, teamwork, and time management skills through both academic study and work experience. I am motivated, dependable, and eager to keep building my technical and analytical abilities.

---

### Education
- **BSc Accounting & Finance**, Bayes Business School (2025–Present)

---

### Key Skills
- Python for Data Analysis  
- Data Visualisation with Plotly  
- Financial Analysis  
- Communication  
- Teamwork  
- Time Management  
- Adaptability  
""")
    return (tab_cv,)


@app.cell
def _(box_chart, cap_slider, hist_chart, mo, scatter_chart, sector_dropdown):
    tab_project = mo.vstack([
        mo.md("""
## 📊 Financial Data Analysis Project

This interactive dashboard analyses the relationship between **credit risk** and **cost of debt** using S&P 500 company data. It allows users to explore how financial strength, measured by the **Altman Z-Score**, affects borrowing costs across sectors and company sizes.

---

### Key Features
- Interactive filtering by **sector**
- Adjustable **market capitalisation threshold**
- Dynamic visualisation of financial relationships
- Multiple interactive charts
- Real-time updates based on user input

---

### Skills Demonstrated
- Data cleaning and transformation using **pandas**
- Interactive UI design using **marimo**
- Data visualisation using **Plotly**
- Financial interpretation of **credit risk metrics**
- Application of the **Altman Z-Score model**

---

### Interpretation
The scatter plot suggests that firms with weaker financial health can face a higher cost of debt.  
The histogram shows how Z-Scores are distributed across selected sectors.  
The box plot helps compare borrowing costs across sectors more clearly.

**Red dashed line:** distress threshold (1.81)  
**Green dashed line:** safe threshold (2.99)

This project demonstrates my ability to combine financial theory with data analysis tools to produce meaningful business insights.
"""),
        mo.callout(
            mo.md("Use the filters below to explore how sector and company size influence credit risk and borrowing costs."),
            kind="info",
        ),
        mo.hstack([sector_dropdown, cap_slider], justify="start", gap=2),
        scatter_chart,
        hist_chart,
        box_chart,
    ])
    return (tab_project,)


@app.cell
def _(mo):
    tab_personal = mo.md("""
## 🌍 Personal Interests

- Painting and drawing  
- Outdoor activities  
- Gym  

These interests help me stay creative, active, and disciplined outside of my academic work.
""")
    return (tab_personal,)


@app.cell
def _(mo, tab_cv, tab_personal, tab_project):
    tabs = mo.ui.tabs({
        "📄 About Me": tab_cv,
        "📊 Projects": tab_project,
        "🌍 Interests": tab_personal,
    })
    return (tabs,)


@app.cell
def _(mo, tabs):
    mo.md(f"""
# Natascia Hossain  
### BSc Accounting & Finance Student | Aspiring Financial Analyst  

Welcome to my personal portfolio website. This platform showcases my work in financial data analysis, where I apply Python, marimo, and data visualisation techniques to explore real-world financial insights.

---
{tabs}
""")
    return


if __name__ == "__main__":
    app.run()