from new_scores import whatsapp_string

def test_normal_string():
    data = {
        "AO5": 42.37,
        "Name": "Test Name",
        "Institute": "Test Institute"
    }

    assert whatsapp_string(data) == "• 42.37 - Test Name - Test Institute"
