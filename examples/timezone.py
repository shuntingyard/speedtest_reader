from speedtest_reader import format_timestamps, Reader, util

sensor1 = Reader("~/speedtest.csv")


@util.append_tslocal(tz="EST")  # zone for local timestamp to append
def slice_EST(**kwargs):
    kwargs["tz"] = "EST"  # zone to use for slicing
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


# use local timezone (selected by module 'tzlocal')
@util.append_tslocal()
def slice_local(**kwargs):
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


# test configured- and local timezone setup
print(slice_EST(start="yesterday"))
print(slice_local(start="yesterday"))
