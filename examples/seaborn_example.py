import matplotlib.pyplot as plt
import seaborn as sns
from speedtest_reader import format_timestamps, Reader, util

sensor1 = Reader("~/speedtest.csv")


@util.to_Mbit
@util.append_mpldate(colname="date2num")
def slice_s1(**kwargs):
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


# minimal scatterplot example
ts = slice_s1()["date2num"]
dl = slice_s1()["Download"]
_, ax = plt.subplots()
sns.scatterplot(ts, dl)
ax.xaxis_date()
plt.show()
