import json
import os
import pytest
from cs50p_reviewer.project import load_module_data, check_answer, calculate_score

def test_load_module_data():
    create_path = "cs50p_reviewer/test_temp_questions.json"
    load_path = "test_temp_questions.json"
    mock_payload = {
        "0": [{"question": "Q1?", "options": [], "answer": "ans1"}]
    }
    with open(create_path, "w") as f:
        json.dump(mock_payload, f)
    try:
        result = load_module_data(load_path, "0")
        assert len(result) == 1
        assert result[0]["answer"] == "ans1"
        with pytest.raises(KeyError):
            load_module_data(load_path, "9")
    finally:
        if os.path.exists(create_path):
            os.remove(create_path)

def test_check_answer():
    assert check_answer("A", "a") is True
    assert check_answer("b", "B") is True
    assert check_answer("strip", "strip") is True
    assert check_answer("A", "B") is False
    assert check_answer(None, "strip") is False

def test_calculate_score():
    assert calculate_score(3, 3) == (100.0, "Pass")
    assert calculate_score(7, 10) == (70.0, "Pass")
    assert calculate_score(2, 3) == (66.7, "Fail")
    assert calculate_score(0, 0) == (0.0, "Fail")
