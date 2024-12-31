import pytest
from fastapi.testclient import TestClient
from ml_service.main import APP

client = TestClient(APP)

def test_mcqa_endpoint():
    payload = {
        "text": "I am so [BLANK].",
        "choice1": "happy",
        "choice2": "sad",
        "choice3": "tired",
        "choice4": "bored"
    }
    response = client.post("/mcqa", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "chosen_label" in json_data
    assert "confidence" in json_data
