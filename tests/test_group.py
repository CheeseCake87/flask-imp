def test_general_setup(client):
    response = client.get('/tests/')
    assert response.status_code == 200


def test_global_route_in_folder(client):
    response = client.get('/')
    assert response.status_code == 200


def test_global_root_file_current_app(client):
    response = client.get('/current-app-import')
    assert response.status_code == 200


def test_global_root_file_factory(client):
    response = client.get('/collection-factory-import')
    assert response.status_code == 200


def test_regular_blueprint(client):
    response = client.get('/regular-blueprint')
    assert response.status_code == 200


def test_nested_blueprint(client):
    response = client.get('/tests/nested_test/')
    assert response.status_code == 200


def test_group_nested_blueprint_one(client):
    response = client.get('/tests/nested_test_one/')
    assert response.status_code == 200


def test_group_nested_blueprint_two(client):
    response = client.get('/tests/nested_test_two/')
    assert response.status_code == 200


def test_error_404(client):
    response = client.get('/tests/error-page-404')
    assert b"No route associated with the URL" in response.data


def test_error_500(client):
    response = client.get('/tests/error-page-500')
    assert b"There has been a server error!" in response.data


def test_context_processors(client):
    response = client.get('/tests/context-processors')
    assert b"$100.00" in response.data


def test_static(client):
    response = client.get('/tests/static')
    assert b"/img/Flask-BigApp-Logo.svg" in response.data


def test_database_creation(client):
    response = client.get('/tests/database-creation')
    assert b"Database created." in response.data


def test_database_population(client):
    response = client.get('/tests/database-population')
    assert b"David created" in response.data


def test_security_login_bool(client):
    client.get('/tests/login/bool')
    response = client.get('/tests/must-be-logged-in/bool')
    assert b"Security" in response.data


def test_security_login_int(client):
    client.get('/tests/login/int')
    response = client.get('/tests/must-be-logged-in/int')
    assert b"Security" in response.data


def test_security_login_str(client):
    client.get('/tests/login/str')
    response = client.get('/tests/must-be-logged-in/str')
    assert b"Security" in response.data


def test_security_login_fail(client):
    client.get('/tests/logout')
    response = client.get('/tests/must-be-logged-in/bool', follow_redirects=True)
    assert b"Login failed" in response.data


def test_permission_list(client):
    client.get('/tests/set-permission/list')
    response = client.get('/tests/must-have-permissions/std')
    assert b"Security" in response.data


def test_permission_value(client):
    client.get('/tests/set-permission/value')
    response = client.get('/tests/must-have-permissions/std')
    assert b"Security" in response.data


def test_permission_fail(client):
    response = client.get('/tests/must-have-permissions/adv', follow_redirects=True)
    assert b"Permission failed" in response.data
