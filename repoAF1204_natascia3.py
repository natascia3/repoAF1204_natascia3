import marimo

__generated_with = "0.22.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    return mo, pd, px


@app.cell
def _(pd):
    csv_url = "https://gist.githubusercontent.com/DrAYim/80393243abdbb4bfe3b45fef58e8d3c8/raw/ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/sp500_ZScore_AvgCostofDebt.csv"

    df = pd.read_csv(csv_url)
    df = df.dropna(subset=['AvgCost_of_Debt', 'Z_Score_lag', 'Sector_Key'])
    df = df[df['AvgCost_of_Debt'] < 5]

    df['Debt_Cost_Percent'] = df['AvgCost_of_Debt'] * 100
    df['Market_Cap_B'] = df['Market_Cap'] / 1e9
    return (df,)


@app.cell
def _(df, mo):
    sectors = sorted(df['Sector_Key'].unique().tolist())

    sector_dropdown = mo.ui.multiselect(
        options=sectors,
        value=sectors[:3],
        label="Filter by Sector"
    )

    cap_slider = mo.ui.slider(
        start=0,
        stop=200,
        step=10,
        value=0,
        label="Min Market Cap ($ Billions)"
    )
    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df, sector_dropdown):
    filtered = df[
        (df['Sector_Key'].isin(sector_dropdown.value)) &
        (df['Market_Cap_B'] >= cap_slider.value)
    ]
    return (filtered,)


@app.cell
def _(filtered, mo, px):
    fig = px.scatter(
        filtered,
        x='Z_Score_lag',
        y='Debt_Cost_Percent',
        color='Sector_Key',
        size='Market_Cap_B',
        hover_name='Name',
        title="Cost of Debt vs Credit Risk",
        template='presentation'
    )

    chart = mo.ui.plotly(fig)
    return (chart,)


@app.cell
def _(mo):
    tab_cv = mo.md("""
    ### Natascia Hossain  
    **Aspiring Financial Analyst | Data & AI Enthusiast**

    ---

    ### Summary
    - Finance student at Bayes Business School with strong interest in financial data analysis.
    - Skilled in Python, marimo, and Plotly for building interactive dashboards.
    - Passionate about using data to support financial decision-making.

    ---

    ### Education
    - BSc Accounting & Finance, Bayes Business School (2025 - Present)

    ---

    ### Skills
    - Python (Data Analysis & Visualisation)
    - Data Visualisation (Plotly, marimo)
    - Financial Analysis
    - Dashboard Development
    """)
    return (tab_cv,)


@app.cell
def _(cap_slider, chart, mo, sector_dropdown):
    tab_project = mo.vstack([
        mo.md("## 📊 Financial Dashboard"),
        mo.callout(mo.md("Explore how credit risk affects borrowing cost"), kind="info"),
        mo.hstack([sector_dropdown, cap_slider]),
        chart
    ])
    return (tab_project,)


@app.cell
def _(mo):
    tab_personal = mo.md("""
    ## 🌍 Personal Interests

    - Travelling and exploring new cultures  
    - Photography  
    - Learning about global markets  
    """)
    return (tab_personal,)


@app.cell
def _(mo, tab_cv, tab_personal, tab_project):
    tabs = mo.ui.tabs({
        "📄 About Me": tab_cv,
        "📊 Projects": tab_project,
        "🌍 Interests": tab_personal
    })

    mo.md(f"""
    # Portfolio Website
    ---
    {tabs}
    """)
    return


if __name__ == "__main__":
    app.run()
