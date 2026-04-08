from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_attitude_endpoint():
    response = client.post(
        "/attitude",
        json={"expression": "5 + 5", "result": "10"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
