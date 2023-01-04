def test_import_builtins(client):
    response = client.get('/tests/')
    assert response.status_code == 200


def test_import_structures(client):
    response = client.get('/tests/static')
    assert b"/theme/static/img/Flask-BigApp-Logo.png" in response.data


# def test_create_all_models(client):
#     response = client.get('/tests/create-all-models')
#     assert response.status_code == 200
#
#
# def test_import_of_models(client):
#     response = client.get('/tests/database-example')
#     assert response.status_code == 200
