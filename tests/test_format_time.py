from new_scores import format_time

def test_small_time():
    assert format_time("00:20.310000") == "20.31"

def test_large_time():
    assert format_time("01:05.300000") == "01:05.30"