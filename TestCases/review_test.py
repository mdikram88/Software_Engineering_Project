# here is the file for creating review test cases
from main import app
import pytest


class TestReviewCases:

    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    def test_get_review_success(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/review/2')
        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == "dict"
        assert "course_id" in json_data["data"]
        assert type(json_data["data"]["course_id"]).__name__ == "int"
        assert "course_name" in json_data["data"]
        assert type(json_data["data"]["course_name"]).__name__ == "str"

    def test_get_review_failure(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/review/23535')
        assert response.status_code == 404
        assert response.json == {
            "message": "Invalid review_id"
        }

    def test_post_review_success(self, client):
        payload = {
            "user_id": 1,
            "course_id": 1,
            "difficulty": 5,
            "support": 3,
            "rating": 4,
            "review": "blab blabalba"
        }

        response = client.post('/api/review', json=payload)
        assert response.status_code == 201
        assert response.json == {
            "message": "Review Added Successfully"
        }

    def test_post_review_failure1(self, client):
        payload = {
            "user_id": "abc",
            "course_id": 1,
            "difficulty": 5,
            "support": 3,
            "rating": 4,
            "review": "blab blabalba"
        }

        response = client.post('/api/review', json=payload)
        assert response.status_code == 400
        assert response.json == {
            "message": "user_id should be integer"
        }

    def test_post_review_failure2(self, client):
        payload = {
            "user_id": 1,
            "course_id": 1,
            "difficulty": 5,

            "rating": 4,
            "review": "blab blabalba"
        }

        response = client.post('/api/review', json=payload)
        assert response.status_code == 404
        assert response.json == {
            "message": "support is required"
        }

    def test_put_review_success(self, client):
        payload = {
            "review_id": 2,
            "difficulty": 1,
            "support": 4,
            "rating": 5,
            "review": "Wonderful"
        }

        response = client.put('/api/review', json=payload)
        assert response.status_code == 202
        assert response.json == {
            "message": "Review Successfully Updated"
        }

    def test_put_review_failure(self, client):
        payload = {
            "review_id": 2,
            "difficulty": 1,
            "support": 4,
            "rating": "wonderful",
            "review": 23
        }

        response = client.put('/api/review', json=payload)
        assert response.status_code == 400
        assert response.json == {
            "message": "rating value should be integer"
        }

    def test_get_student_review_success(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/reviews/student/1')
        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == "list"
        assert "course_id" in json_data["data"][0]
        assert type(json_data["data"][0]["course_id"]).__name__ == "int"
        assert "course_name" in json_data["data"][0]
        assert type(json_data["data"][0]["course_name"]).__name__ == "str"

    def test_get_student_review_failure(self, client):
        # Simulate a GET request to the '/' route
        response = client.get('/api/reviews/student/11')
        assert response.status_code == 404
        assert response.json == {
            "message": "Invalid user_id"
        }

    def test_del_review_success(self, client):
        response = client.delete('/api/review/5')
        assert response.status_code == 200
        assert response.json == {
            "message": "Review Deleted Successfully"
        }

    def test_del_review_failure(self, client):
        response = client.delete('/api/review/100', )
        assert response.status_code == 404
        assert response.json == {
            "message": "Invalid Review Id"
        }
