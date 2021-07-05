from new_scores import ao5_calc

def test_all_five_times_with_default_event_1():
    times = {
        "e1t1": 19.34,
        "e1t2": 18.20,
        "e1t3": 21.49,
        "e1t4": 20.01,
        "e1t5": 17.78
    }

    assert ao5_calc(times) == 19.18

def test_all_five_times_with_specified_event():
    times = {
        "e3t1": 19.34,
        "e3t2": 18.20,
        "e3t3": 21.49,
        "e3t4": 20.01,
        "e3t5": 17.78
    }

    assert ao5_calc(times, event=3) == 19.18

def test_one_dnf():
    times = {
        "e2t1": 19.34,
        "e2t2": "DNF",
        "e2t3": 21.49,
        "e2t4": 20.01,
        "e2t5": 17.78
    }

    assert ao5_calc(times, event=2) == 20.28

def test_two_dnf():
    times = {
        "e2t1": 19.34,
        "e2t2": "DNF",
        "e2t3": 21.49,
        "e2t4": "DNF",
        "e2t5": 17.78
    }

    assert ao5_calc(times, event=2) == "DNF"

def test_one_dns():
    times = {
        "e2t1": 19.34,
        "e2t2": "DNS",
        "e2t3": 21.49,
        "e2t4": 20.01,
        "e2t5": 17.78
    }

    assert ao5_calc(times, event=2) == 20.28

def test_two_dns():
    times = {
        "e2t1": 19.34,
        "e2t2": "DNS",
        "e2t3": 21.49,
        "e2t4": "DNS",
        "e2t5": 17.78
    }

    assert ao5_calc(times, event=2) == "DNF"

def test_dnf_and_dns():
    times = {
        "e2t1": 19.34,
        "e2t2": "DNS",
        "e2t3": 21.49,
        "e2t4": "DNF",
        "e2t5": 17.78
    }

    assert ao5_calc(times, event=2) == "DNF"