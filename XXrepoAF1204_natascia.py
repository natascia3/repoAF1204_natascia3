import marimo

__generated_with = "0.22.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import plotly.express as px
    import pandas as pd
    return mo, pd, px


@app.cell
def _(px):
    df = px.data.gapminder()
    years = sorted(df["year"].unique())
    continents = ["All"] + sorted(df["continent"].unique())
    return continents, df, years


@app.cell
def _(mo):
    mo.md("""
# Natascia's Data Portfolio

I am a finance student interested in financial data analysis, visualisation, and using Python to turn data into clear insights.
""")
    return


@app.cell
def _(mo):
    mo.md("""
## About Me

This project shows my skills in:

- Python
- marimo
- plotly
- interactive visualisation
- filtering and comparing data
""")
    return


@app.cell
def _(mo):
    mo.md("""
## Project Overview

This dashboard explores country-level development indicators using interactive data visualisations.
""")
    return


@app.cell
def _(continents, mo, years):
    year = mo.ui.slider(
        start=min(years),
        stop=max(years),
        step=5,
        value=max(years),
        label="Select year",
    )

    continent = mo.ui.dropdown(
        options=continents,
        value="All",
        label="Select continent",
    )

    mo.vstack([year, continent])
    return continent, year


@app.cell
def _(continent, df, year):
    filtered = df[df["year"] == year.value]
    if continent.value != "All":
        filtered = filtered[filtered["continent"] == continent.value]
    return filtered


@app.cell
def _(continent, mo, year):
    mo.md(f"""
## Interactive Dashboard

**Selected year:** {year.value}  
**Selected continent:** {continent.value}
""")
    return


@app.cell
def _(filtered, mo, px):
    scatter_fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        title="Scatter Plot: GDP per Capita vs Life Expectancy",
        log_x=True,
    )
    mo.ui.plotly(scatter_fig)
    return


@app.cell
def _(filtered, mo, px):
    hist_fig = px.histogram(
        filtered,
        x="lifeExp",
        color="continent",
        nbins=20,
        title="Histogram: Distribution of Life Expectancy",
    )
    mo.ui.plotly(hist_fig)
    return


@app.cell
def _(filtered, mo, px):
    top10 = filtered.sort_values("pop", ascending=False).head(10)

    bar_fig = px.bar(
        top10,
        x="country",
        y="pop",
        color="continent",
        title="Bar Chart: Top 10 Countries by Population",
    )
    mo.ui.plotly(bar_fig)
    return


@app.cell
def _(continent, df, mo, px):
    if continent.value == "All":
        avg = df.groupby(["year", "continent"], as_index=False)["lifeExp"].mean()
        line_fig = px.line(
            avg,
            x="year",
            y="lifeExp",
            color="continent",
            title="Line Chart: Average Life Expectancy Over Time by Continent",
        )
    else:
        avg = df[df["continent"] == continent.value]
        avg = avg.groupby("year", as_index=False)["lifeExp"].mean()
        line_fig = px.line(
            avg,
            x="year",
            y="lifeExp",
            title=f"Line Chart: Average Life Expectancy Over Time in {continent.value}",
        )

    mo.ui.plotly(line_fig)
    return


@app.cell
def _(filtered, mo, px):
    pie_data = filtered.groupby("continent", as_index=False)["pop"].sum()

    pie_fig = px.pie(
        pie_data,
        names="continent",
        values="pop",
        title="Pie Chart: Population Share by Continent",
    )
    mo.ui.plotly(pie_fig)
    return


@app.cell
def _(filtered, mo, px):
    density_fig = px.density_contour(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        color="continent",
        title="Density Plot: GDP per Capita and Life Expectancy",
    )
    mo.ui.plotly(density_fig)
    return


@app.cell
def _(filtered, mo, px):
    box_fig = px.box(
        filtered,
        x="continent",
        y="lifeExp",
        color="continent",
        title="Box Plot: Life Expectancy by Continent",
    )
    mo.ui.plotly(box_fig)
    return


@app.cell
def _(mo):
    mo.md("""
## Finance Visualisation

This section shows finance-related plots using technology stock data.
""")
    return


@app.cell
def _(px):
    stocks = px.data.stocks()
    return stocks


@app.cell
def _(mo):
    stock = mo.ui.dropdown(
        options=["AAPL", "GOOG", "AMZN", "FB", "NFLX", "MSFT"],
        value="AAPL",
        label="Select stock",
    )
    stock
    return stock


@app.cell
def _(stock, stocks):
    finance_df = stocks[["date", stock.value]].copy()
    finance_df.columns = ["date", "price"]
    finance_df["return"] = finance_df["price"].pct_change()
    finance_df = finance_df.dropna()
    return finance_df


@app.cell
def _(finance_df, mo, px, stock):
    fin_line_fig = px.line(
        finance_df,
        x="date",
        y="price",
        title=f"Finance Line Chart: {stock.value} Price Over Time",
    )
    mo.ui.plotly(fin_line_fig)
    return


@app.cell
def _(finance_df, mo, px, stock):
    fin_scatter_fig = px.scatter(
        finance_df,
        x="date",
        y="price",
        title=f"Finance Scatter Plot: {stock.value} Price Over Time",
    )
    mo.ui.plotly(fin_scatter_fig)
    return


@app.cell
def _(finance_df, mo, px, stock):
    fin_hist_fig = px.histogram(
        finance_df,
        x="return",
        nbins=30,
        title=f"Finance Histogram: {stock.value} Returns",
    )
    mo.ui.plotly(fin_hist_fig)
    return


@app.cell
def _(finance_df, mo, px, stock):
    fin_box_fig = px.box(
        finance_df,
        y="return",
        title=f"Finance Box Plot: {stock.value} Returns",
    )
    mo.ui.plotly(fin_box_fig)
    return


@app.cell
def _(mo):
    mo.md("""
## Key Insights

- Countries with higher GDP per capita often have higher life expectancy.
- Population is concentrated in a small number of countries.
- Continents show different development patterns.
- Stock prices and returns can also be explored using visual tools.
""")
    return


@app.cell
def _(mo):
    mo.md("""
## Contact

- Name: Natascia Hossain
- Course: AF1204 Introduction to Data Science and AI Tools
- Tools used: Python, marimo, plotly

Thank you for viewing my portfolio webpage.
""")
    return


if __name__ == "__main__":
    app.run()