# here is the file for creating user test cases
from main import app
import pytest


class TestUserCases:

    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    def test_hello(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/course/1')

        assert response.status_code == 200

    def admin_course_list_success(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/admin_courses_list')

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == 'list'


