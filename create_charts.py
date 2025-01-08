import altair as alt
import pandas as pd
from custom import *


def create_linechart(df: pd.DataFrame, reg: int) -> pd.DataFrame:
    y_min = min(df['count'].min(), df['regression'].min())
    y_max = max(df['count'].max(), df['regression'].max())

    chart = alt.Chart(df).mark_line(color='#A9B84A').encode(
        x=alt.X('datum:T', title='Datum', axis=alt.Axis(format='%Y-%m', labelAngle=-90)),
        y=alt.Y('count:Q', title='Anzahl', scale=alt.Scale(domain=(y_min, y_max)))
    )

    if(reg == False):
        return chart
    else:

        regression_line = alt.Chart(df).mark_line(color='#E3000F').encode(
            x=alt.X('datum:T'),
            y=alt.Y('regression:Q', title="Trend")
        )

        combined_chart = alt.layer(chart, regression_line).encode(
            x='datum',
            y=alt.Y('count:Q', scale=alt.Scale(domain=(y_min, y_max))),
        )
        return combined_chart