from pathlib import Path

import pytest

from test_app import create_app

instance_folder = Path(__file__).parent / "test_app" / "instance"

if not instance_folder.exists():
    instance_folder.mkdir()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
