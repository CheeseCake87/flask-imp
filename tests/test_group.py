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
    assert b"/img/Flask-Imp-Small.png" in response.data


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


def test_security_login_fail_with_message(client):
    client.get('/tests/logout')
    response = client.get('/tests/must-be-logged-in/bool/with-flash', follow_redirects=True)
    assert b"message:Login needed" in response.data


def test_security_already_logged_in_pass_with_message(client):
    client.get('/tests/login/bool')
    response = client.get('/tests/already-logged-in/bool/with-flash', follow_redirects=True)
    assert b"message:Already logged in" in response.data


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


def test_csrf_pass(client):
    session = client.get('/tests/csrf-session')
    response = client.post(
        '/tests/csrf-post-pass', data={'csrf': session.data.decode('utf-8')}
    )
    assert response.status_code == 200


def test_csrf_fail(client):
    client.get('/tests/csrf-session')
    response = client.post(
        '/tests/csrf-post-fail', data={'csrf': '000'}
    )
    assert response.status_code == 401


def test_pass_function_check_missing_kwargs_ignored(client):
    response = client.get('/tests/pass-func-check')
    assert b"Pass" in response.data


def test_pass_function_check_fail_on_missing_kwargs(client):
    response = client.get('/tests/pass-func-check-fail-on-kwargs', follow_redirects=True)
    assert b"Permission failed" in response.data


def test_pass_function_check_with_url_value(client):
    response = client.get('/tests/pass-func-check-with-url-var-replaced/100', follow_redirects=True)
    assert b"URL value: 100" in response.data


def test_pass_function_check_with_url_value_with_ac(client):
    response = client.get('/tests/pass-func-check-with-url-var-replaced-and-app-context/100', follow_redirects=True)
    assert b"URL value: 100" in response.data


def test_password_encryption_authentication_correct(client):
    response = client.get('/tests/auth/password/correct', follow_redirects=True)
    assert b"True" in response.data


def test_password_encryption_authentication_incorrect(client):
    response = client.get('/tests/auth/password/incorrect', follow_redirects=True)
    assert b"False" in response.data


def test_password_encryption_authentication_correct_long(client):
    response = client.get('/tests/auth/password/correct/long', follow_redirects=True)
    assert b"True" in response.data
