def test_import_builtins(client):
    response = client.get('/tests/')
    assert response.status_code == 200


def test_import_structures(client):
    response = client.get('/tests/static')
    assert b"/img/Flask-BigApp-Logo.png" in response.data
