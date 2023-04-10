def test_general_setup(client):
    """
    If this test is successful, the app is set up and running correctly.
    """
    response = client.get('/tests/')
    assert response.status_code == 200


def test_error_404(client):
    """
    If this test is successful, the app is set up and running correctly.
    """
    response = client.get('/tests/error-page-404')
    assert b"No route associated with the URL" in response.data


def test_error_500(client):
    """
    If this test is successful, the app is set up and running correctly.
    """
    response = client.get('/tests/error-page-500')
    assert b"There has been a server error!" in response.data


def test_context_processors(client):
    """
    If this test is successful, the context processors are working correctly.
    """
    response = client.get('/tests/context-processors')
    assert b"$100.00" in response.data


def test_import_theme(client):
    """
    If this test is successful, the import of the theme is working correctly.
    """
    response = client.get('/tests/static')
    assert b"/img/Flask-BigApp-Logo.png" in response.data


def test_database_creation(client):
    """
    If this test is successful, the database has been dropped and created correctly.
    """
    response = client.get('/tests/database-creation')
    assert b"Database created." in response.data


def test_mixin_create(client):
    """
    If this test is successful, the mixin is working correctly.
    """
    response = client.get('/tests/mixin-add')
    assert b"MixinTest" in response.data


def test_database_population(client):
    """
    If this test is successful, the database has been populated correctly.
    """
    response = client.get('/tests/database-population')
    assert b"David created" in response.data
