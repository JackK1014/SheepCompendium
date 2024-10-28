from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Sugar",
        "breed": "suffolk",
        "sex": "ewe"
    }
    response = client.post("/sheep/", json=new_sheep_data)
    assert response.status_code == 201
    assert response.json() == new_sheep_data
    new_sheep = client.get(f"/sheep/{new_sheep_data['id']}")
    assert new_sheep.status_code == 200


def test_delete_sheep():
    sheep_to_delete = {
        "id": 20,
        "name": "Honey",
        "breed": "merino",
        "sex": "ewe"
    }
    client.post("/sheep/", json=sheep_to_delete)

    delete_response = client.delete(f"/sheep/{sheep_to_delete['id']}")
    assert delete_response.status_code == 204

    confirm_delete = client.delete(f"/sheep/{sheep_to_delete['id']}")
    assert confirm_delete.status_code == 404


def test_update_sheep():
    sheep_to_update = {
        "id": 9,
        "name": "Fluffy",
        "breed": "finnsheep",
        "sex": "ram"
    }
    client.post("/sheep/", json=sheep_to_update)

    updated_sheep_data = {
        "id": 9,
        "name": "New Fluffy",
        "breed": "finnsheep",
        "sex": "ram"
    }
    update_response = client.put(f"/sheep/{sheep_to_update['id']}", json=updated_sheep_data)
    assert update_response.status_code == 200
    assert update_response.json() == updated_sheep_data

    confirm_update = client.get(f"/sheep/{sheep_to_update['id']}")
    assert confirm_update.status_code == 200
    assert confirm_update.json() == updated_sheep_data


def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 6
