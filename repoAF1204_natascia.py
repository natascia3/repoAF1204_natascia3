import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import plotly.express as px
    return mo, px


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
def _(mo, years, continents):
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
def _(df, year, continent):
    filtered = df[df["year"] == year.value]

    if continent.value != "All":
        filtered = filtered[filtered["continent"] == continent.value]

    return filtered,


@app.cell
def _(mo, year, continent):
    mo.md(f"""
## Interactive Dashboard

**Selected year:** {year.value}  
**Selected continent:** {continent.value}
""")
    return


@app.cell
def _(filtered, px):
    fig_scatter = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        title="Scatter Plot: GDP per Capita vs Life Expectancy",
        log_x=True,
    )
    fig_scatter
    return


@app.cell
def _(filtered, px):
    fig_hist = px.histogram(
        filtered,
        x="lifeExp",
        color="continent",
        nbins=20,
        title="Histogram: Distribution of Life Expectancy",
    )
    fig_hist
    return


@app.cell
def _(filtered, px):
    top10 = filtered.sort_values("pop", ascending=False).head(10)

    fig_bar = px.bar(
        top10,
        x="country",
        y="pop",
        color="continent",
        title="Bar Chart: Top 10 Countries by Population",
    )
    fig_bar
    return


@app.cell
def _(df, continent, px):
    if continent.value == "All":
        avg = df.groupby(["year", "continent"], as_index=False)["lifeExp"].mean()
        fig_line = px.line(
            avg,
            x="year",
            y="lifeExp",
            color="continent",
            title="Line Chart: Average Life Expectancy Over Time by Continent",
        )
    else:
        avg = df[df["continent"] == continent.value]
        avg = avg.groupby("year", as_index=False)["lifeExp"].mean()
        fig_line = px.line(
            avg,
            x="year",
            y="lifeExp",
            title=f"Line Chart: Average Life Expectancy Over Time in {continent.value}",
        )

    fig_line
    return


@app.cell
def _(filtered, px):
    pie = filtered.groupby("continent", as_index=False)["pop"].sum()

    fig_pie = px.pie(
        pie,
        names="continent",
        values="pop",
        title="Pie Chart: Population Share by Continent",
    )
    fig_pie
    return


@app.cell
def _(filtered, px):
    fig_density = px.density_contour(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        color="continent",
        title="Density Plot: GDP per Capita and Life Expectancy",
    )
    fig_density
    return


@app.cell
def _(filtered, px):
    fig_box = px.box(
        filtered,
        x="continent",
        y="lifeExp",
        color="continent",
        title="Box Plot: Life Expectancy by Continent",
    )
    fig_box
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
    return stocks,


@app.cell
def _(mo):
    stock = mo.ui.dropdown(
        options=["AAPL", "GOOG", "AMZN", "FB", "NFLX", "MSFT"],
        value="AAPL",
        label="Select stock",
    )
    stock
    return stock,


@app.cell
def _(stocks, stock):
    finance_df = stocks[["date", stock.value]].copy()
    finance_df.columns = ["date", "price"]
    finance_df["return"] = finance_df["price"].pct_change()
    finance_df = finance_df.dropna()
    return finance_df,


@app.cell
def _(finance_df, stock, px):
    fig_fin_line = px.line(
        finance_df,
        x="date",
        y="price",
        title=f"Finance Line Chart: {stock.value} Price Over Time",
    )
    fig_fin_line
    return


@app.cell
def _(finance_df, stock, px):
    fig_fin_scatter = px.scatter(
        finance_df,
        x="date",
        y="price",
        title=f"Finance Scatter Plot: {stock.value} Price Over Time",
    )
    fig_fin_scatter
    return


@app.cell
def _(finance_df, stock, px):
    fig_fin_hist = px.histogram(
        finance_df,
        x="return",
        nbins=30,
        title=f"Finance Histogram: {stock.value} Returns",
    )
    fig_fin_hist
    return


@app.cell
def _(finance_df, stock, px):
    fig_fin_box = px.box(
        finance_df,
        y="return",
        title=f"Finance Box Plot: {stock.value} Returns",
    )
    fig_fin_box
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