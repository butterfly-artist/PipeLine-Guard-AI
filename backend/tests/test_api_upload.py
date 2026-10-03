from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_profile_api_upload():
    csv_content = "id,name,value\n1,alpha,10.0\n2,beta,20.0\n"
    response = client.post(
        "/api/profile",
        files={"file": ("localities.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 2
    assert data["column_count"] == 3


def test_analyze_api_upload():
    csv_content = "id,name,value\n1,alpha,10.0\n2,beta,20.0\n"
    response = client.post(
        "/api/analyze",
        files=[
            ("files", ("localities.csv", csv_content, "text/csv"))
        ]
    )
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert "dq_results" in data
    assert "diagnosis" in data
