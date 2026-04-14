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
def _(pd):
    csv_url = "https://gist.githubusercontent.com/DrAYim/80393243abdbb4bfe3b45fef58e8d3c8/raw/ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/sp500_ZScore_AvgCostofDebt.csv"

    df = pd.read_csv(csv_url)

    df = df.dropna(
        subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key", "Market_Cap", "Name"]
    ).copy()

    df = df[df["AvgCost_of_Debt"] < 0.15].copy()

    df["Debt_Cost_Percent"] = df["AvgCost_of_Debt"] * 100
    df["Market_Cap_B"] = df["Market_Cap"] / 1e9
    df["Z_Score_lag"] = df["Z_Score_lag"].round(2)
    df["Debt_Cost_Percent"] = df["Debt_Cost_Percent"].round(2)
    df["Market_Cap_B"] = df["Market_Cap_B"].round(2)

    def classify_zone(z):
        if z < 1.81:
            return "Distress Zone"
        elif z < 2.99:
            return "Grey Zone"
        else:
            return "Safe Zone"

    df["Risk_Zone"] = df["Z_Score_lag"].apply(classify_zone)

    return (df,)


@app.cell
def _(df, mo):
    sectors = sorted(df["Sector_Key"].unique().tolist())

    max_cap = int((df["Market_Cap_B"].max() // 50 + 1) * 50)

    sector_dropdown = mo.ui.multiselect(
        options=sectors,
        value=sectors[:4],
        label="Filter by Sector",
    )

    cap_slider = mo.ui.slider(
        start=0,
        stop=max_cap,
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
def _(filtered):
    company_count = len(filtered)

    if company_count > 0:
        avg_debt_cost = round(filtered["Debt_Cost_Percent"].mean(), 2)
        median_z = round(filtered["Z_Score_lag"].median(), 2)
        distressed_pct = round(
            (filtered["Risk_Zone"].eq("Distress Zone").mean() * 100), 1
        )
    else:
        avg_debt_cost = 0
        median_z = 0
        distressed_pct = 0

    return avg_debt_cost, company_count, distressed_pct, median_z


@app.cell
def _(avg_debt_cost, company_count, distressed_pct, median_z, mo):
    kpi_row = mo.hstack(
        [
            mo.callout(
                mo.md(f"### {company_count}\n**Companies Selected**"),
                kind="neutral",
            ),
            mo.callout(
                mo.md(f"### {avg_debt_cost}%\n**Average Cost of Debt**"),
                kind="info",
            ),
            mo.callout(
                mo.md(f"### {median_z}\n**Median Altman Z-Score**"),
                kind="warn",
            ),
            mo.callout(
                mo.md(f"### {distressed_pct}%\n**In Distress Zone**"),
                kind="danger",
            ),
        ],
        widths="equal",
        gap=2,
    )
    return (kpi_row,)


@app.cell
def _(filtered, mo, px):
    fig = px.scatter(
        filtered,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        size="Market_Cap_B",
        hover_name="Name",
        hover_data={
            "Sector_Key": True,
            "Market_Cap_B": ":.2f",
            "Risk_Zone": True,
            "Z_Score_lag": ":.2f",
            "Debt_Cost_Percent": ":.2f",
        },
        title="Cost of Debt vs Credit Risk",
        labels={
            "Z_Score_lag": "Altman Z-Score",
            "Debt_Cost_Percent": "Cost of Debt (%)",
            "Sector_Key": "Sector",
            "Market_Cap_B": "Market Cap ($B)",
        },
        template="presentation",
        width=950,
        height=620,
    )

    fig.add_vline(x=1.81, line_dash="dash", line_color="red")
    fig.add_vline(x=2.99, line_dash="dash", line_color="green")

    fig.add_annotation(
        x=1.81,
        y=1.02,
        yref="paper",
        text="Distress threshold",
        showarrow=False,
        font=dict(size=11),
    )

    fig.add_annotation(
        x=2.99,
        y=1.02,
        yref="paper",
        text="Safe threshold",
        showarrow=False,
        font=dict(size=11),
    )

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
        width=950,
        height=500,
        barmode="overlay",
        opacity=0.72,
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
        width=950,
        height=560,
        points="outliers",
    )

    box_fig.update_layout(xaxis_tickangle=-30)

    box_chart = mo.ui.plotly(box_fig)
    return (box_chart,)


@app.cell
def _(filtered, mo, px):
    risk_summary = (
        filtered.groupby("Risk_Zone", as_index=False)["Debt_Cost_Percent"]
        .mean()
        .sort_values("Debt_Cost_Percent", ascending=False)
    )

    zone_order = ["Distress Zone", "Grey Zone", "Safe Zone"]

    risk_bar_fig = px.bar(
        risk_summary,
        x="Risk_Zone",
        y="Debt_Cost_Percent",
        color="Risk_Zone",
        category_orders={"Risk_Zone": zone_order},
        title="Average Cost of Debt by Risk Zone",
        labels={
            "Risk_Zone": "Risk Zone",
            "Debt_Cost_Percent": "Average Cost of Debt (%)",
        },
        template="presentation",
        width=950,
        height=500,
        text_auto=".2f",
    )

    risk_bar_chart = mo.ui.plotly(risk_bar_fig)
    return (risk_bar_chart,)


@app.cell
def _(filtered, mo):
    if len(filtered) == 0:
        top_risk_md = mo.md("No companies match the selected filters.")
    else:
        top_risk = filtered.nsmallest(5, "Z_Score_lag")[
            [
                "Name",
                "Sector_Key",
                "Z_Score_lag",
                "Debt_Cost_Percent",
                "Market_Cap_B",
                "Risk_Zone",
            ]
        ].copy()

        lines = []
        for _, row in top_risk.iterrows():
            lines.append(
                f"- **{row['Name']}** ({row['Sector_Key']}) — "
                f"Z-Score: **{row['Z_Score_lag']}**, "
                f"Cost of Debt: **{row['Debt_Cost_Percent']}%**, "
                f"Market Cap: **${row['Market_Cap_B']}B**, "
                f"Zone: **{row['Risk_Zone']}**"
            )

        top_risk_md = mo.md(
            "### Highest-Risk Companies in Current Selection\n\n"
            + "\n".join(lines)
        )

    return (top_risk_md,)


@app.cell
def _(filtered, mo):
    if len(filtered) == 0:
        insight_text = """
### Analytical Insight
No observations are available under the current filters. Try selecting more sectors or lowering the market capitalisation threshold.
"""
    else:
        distress = filtered[filtered["Risk_Zone"] == "Distress Zone"]
        safe = filtered[filtered["Risk_Zone"] == "Safe Zone"]

        if len(distress) > 0:
            distress_avg = round(distress["Debt_Cost_Percent"].mean(), 2)
        else:
            distress_avg = None

        if len(safe) > 0:
            safe_avg = round(safe["Debt_Cost_Percent"].mean(), 2)
        else:
            safe_avg = None

        largest_sector = filtered["Sector_Key"].value_counts().idxmax()

        if distress_avg is not None and safe_avg is not None:
            spread = round(distress_avg - safe_avg, 2)
            insight_text = f"""
### Analytical Insight
The filtered data suggests a meaningful relationship between **financial health** and **borrowing cost**.  
Companies in the **Distress Zone** have an average cost of debt of **{distress_avg}%**, compared with **{safe_avg}%** for firms in the **Safe Zone**.  
This implies a borrowing cost gap of **{spread} percentage points**, supporting the idea that lenders demand higher returns from firms with weaker balance-sheet strength.

The largest group in the current selection is **{largest_sector}**, which means the sector mix can materially affect the overall distribution shown in the charts.  
Overall, the dashboard indicates that stronger Altman Z-Scores are generally associated with lower financing pressure and better credit quality.
"""
        else:
            insight_text = f"""
### Analytical Insight
The current filtered view does not include enough firms in both the **Distress Zone** and **Safe Zone** to compare average borrowing costs directly.  
However, the selected companies still show how sector composition and company size can influence the distribution of Altman Z-Scores and cost of debt.

The largest group in the current selection is **{largest_sector}**.  
This dashboard remains useful for identifying which sectors contain more financially vulnerable firms and where borrowing costs appear most dispersed.
"""

    insight_md = mo.md(insight_text)
    return (insight_md,)


@app.cell
def _(mo):
    tab_cv = mo.md("""
### Natascia Hossain  
**BSc Accounting & Finance Student | Aspiring Financial Analyst**

---

### Professional Profile
I am a BSc Accounting and Finance student at Bayes Business School with a strong interest in financial analysis, Python, marimo, and data visualisation. I enjoy using data tools to explore real-world business problems and communicate insights clearly.

Through academic coursework and work experience, I have developed strong communication, teamwork, adaptability, and time management skills. I am motivated to continue building both my technical and analytical abilities.

---

### Education
- **BSc Accounting & Finance**, Bayes Business School (2025–Present)

---

### Key Skills
- Python for Data Analysis  
- Data Visualisation with Plotly  
- Financial Analysis  
- Interactive Dashboards with marimo  
- Communication  
- Teamwork  
- Time Management  
- Adaptability  
""")
    return (tab_cv,)


@app.cell
def _(
    box_chart,
    cap_slider,
    hist_chart,
    insight_md,
    kpi_row,
    mo,
    risk_bar_chart,
    scatter_chart,
    sector_dropdown,
    top_risk_md,
):
    tab_project = mo.vstack([
        mo.md("""
## 📊 Financial Data Analysis Project

This interactive portfolio project investigates the relationship between **credit risk** and **cost of debt** using S&P 500 company data. The analysis focuses on the **Altman Z-Score** as a measure of financial health and examines how borrowing costs vary across sectors and company sizes.

---

### Project Aim
The purpose of this dashboard is to show how financial strength can influence a firm's access to external finance. In particular, it explores whether firms with lower Z-Scores, indicating greater financial distress, tend to face higher borrowing costs.

---

### Skills Demonstrated
- Data cleaning and transformation using **pandas**
- Interactive dashboard design using **marimo**
- Financial visualisation using **Plotly**
- Application of the **Altman Z-Score** to assess default risk
- Comparative analysis across sectors and market capitalisation ranges
- Interpretation of credit risk patterns for business decision-making

---

### Why This Project Stands Out
This project combines financial theory with interactive data analysis rather than only presenting static charts. Users can adjust the sector mix and firm size threshold to test how conclusions change under different market conditions. This makes the dashboard more analytical, exploratory, and suitable for professional portfolio use.

**Red dashed line:** Distress threshold (**1.81**)  
**Green dashed line:** Safe threshold (**2.99**)
"""),
        mo.callout(
            mo.md(
                "Use the controls below to explore how **sector** and **company size** influence credit risk and borrowing costs."
            ),
            kind="info",
        ),
        kpi_row,
        mo.hstack([sector_dropdown, cap_slider], justify="start", gap=2),
        scatter_chart,
        hist_chart,
        box_chart,
        risk_bar_chart,
        insight_md,
        top_risk_md,
        mo.callout(
            mo.md("""
### Conclusion
Overall, the dashboard suggests that firms with weaker financial health generally face **higher borrowing costs**, while firms in stronger financial positions tend to benefit from cheaper access to debt finance. This supports the view that credit quality is an important determinant of corporate financing conditions.

The project demonstrates my ability to use Python-based tools to transform financial data into clear, interactive, and decision-relevant insights.
"""),
            kind="success",
        ),
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