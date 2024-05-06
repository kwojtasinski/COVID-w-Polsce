from fastapi.testclient import TestClient


def test_get_df(client: TestClient):
    response = client.get("/get-df?year=2020")
    assert response.status_code == 200
    assert response.text == '"test"'
    second_response = client.get("/get-df?year=2020")
    assert second_response.status_code == 200
    assert second_response.text == '"test"'
