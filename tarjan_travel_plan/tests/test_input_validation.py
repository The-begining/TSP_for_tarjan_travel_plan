import pytest
from tarjan_travel_plan.tarjanplanner.main import validate_input_regex

def test_validate_input_regex_valid():
    valid_input = "single"
    pattern = r"^(single|mixed-time|mixed-cost|balanced)$"
    assert validate_input_regex(valid_input, pattern, "Invalid input") == valid_input

def test_validate_input_regex_invalid():
    invalid_input = "random"
    pattern = r"^(single|mixed-time|mixed-cost|balanced)$"
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input_regex(invalid_input, pattern, "Invalid input")
