import time
from os import environ

import docker as docker
import pytest

from app import create_app
from tables import User, db

POSTGRES_PASSWORD = "supersecretpassword"
PORT = 65432
USER = "postgres"
DB = "postgres"


@pytest.fixture(scope="session")
def database():
    """Create and configure a test database instance."""
    client = docker.from_env()
    container = client.containers.run(
        image="postgres:12",
        auto_remove=True,
        environment=dict(
            POSTGRES_PASSWORD=POSTGRES_PASSWORD,
        ),
        name="test_postgres",
        ports={"5432/tcp": ("127.0.0.1", PORT)},
        detach=True,
        remove=True,
    )

    # Wait for the container to start
    # (actually I use more complex check to wait for container to start but it doesn't really matter)
    time.sleep(5)

    yield

    container.stop()


@pytest.fixture(scope="session")
def test_app(database):
    """Create and configure a test app instance."""
    environ.setdefault('DB_URL', f'postgresql://{USER}:{POSTGRES_PASSWORD}@localhost:{PORT}/{DB}')
    flask_app_instance = create_app().app
    flask_app_instance.config['TESTING'] = True
    yield flask_app_instance


@pytest.fixture(scope="session")
def init_db_data(test_app):
    default_user = User(password='65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5')
    with test_app.app_context():
        db.session.add(default_user)
        db.session.commit()


@pytest.fixture(scope="module")
def client(init_db_data, test_app):
    """Create a test client for the app."""
    return test_app.test_client()


@pytest.fixture(scope="function")
def example_task_data():
    """Example task data for testing."""
    return {
        "title": "Test Task",
        "status": "to_do"
    }
