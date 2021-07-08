from new_scores import whatsapp_string

def test_normal_string():
    data = {
        "AO5": 42.37,
        "Name": "Test Name",
        "Institute": "Test Institute"
    }

    assert whatsapp_string(data) == "• 42.37 - Test Name - Test Institute"

def test_dnf_string():
    data = {
        "AO5": "DNF",
        "Name": "Test Name",
        "Institute": "Test Institute"
    }

    assert whatsapp_string(data) == "• DNF - Test Name - Test Institute"

def test_missing_institute():
    data = {
        "AO5": 42.37,
        "Name": "Test Name",
        "Institute": ""
    }

    assert whatsapp_string(data) == "• 42.37 - Test Name"