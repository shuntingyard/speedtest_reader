from speedtest_reader import format_timestamps, Reader, util

sensor1 = Reader("~/speedtest.csv")


@util.to_Mbit
def slice_s1(**kwargs):
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


# Test API setup
print(slice_s1(start="2019-06-01"))
print(slice_s1(start="July 1", end="July 3"))
print(slice_s1(start="yesterday"))
