def test_import_builtins(client):
    response = client.get('/test-builtin')
    assert response.status_code == 200


def test_import_structures(client):
    response = client.get('/test-structure')
    assert b"/default_theme/static/img/Flask-BigApp-Logo.png" in response.data


def test_create_all_models(client):
    response = client.get('/create-all-models')
    assert response.status_code == 200


def test_import_of_models(client):
    response = client.get('/database-example')
    assert response.status_code == 200
