import plotly
import plotly.graph_objs as go
from speedtest_reader import format_timestamps, Reader, util

sensor1 = Reader("~/speedtest.csv")


@util.append_tslocal()
def slice_s1(**kwargs):
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


# minimal line- and scatterplot example
df = slice_s1()
graph = dict(
    data=[
        go.Scatter(
            x=df["tslocal"], y=df["Download"], mode="lines", connectgaps=False
        ),
        go.Scatter(x=df["tslocal"], y=df["Upload"], mode="markers"),
    ]
)
plotly.offline.plot(graph)
