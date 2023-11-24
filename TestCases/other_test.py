import pytest
import json
from main import app


class TestOtherCases:

    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    # ------------------------------------------ GET ------------------------------------------
    def test_admin_course_list_success(self, client):
        response = client.get('/api/admin_courses_list')

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == 'list'
        assert type(json_data["data"][0]).__name__ == 'dict'
        assert json_data["data"][0] == {
                                            "avg_difficulty": 3.0,
                                            "avg_rating": 2.5,
                                            "code": "CS001214",
                                            "course_id": 1,
                                            "course_type": "Diploma in Programming",
                                            "description": "bla bla bla bla4",
                                            "duration": "12 weeks",
                                            "is_active": True,
                                            "level": "1",
                                            "name": "Java",
                                            "professor": "Someone",
                                            "support": 2.0
                                        }

    def test_update_course_status_success(self, client):
        payload = {"course_id": 2}
        response = client.put('/api/update_course_status', json=payload)

        assert response.status_code == 200
        assert response.json == {"message": "Status Updated Successfully"}

    def test_update_course_status_invalid_id(self, client):
        payload = {"course_id": -1}
        response = client.put('/api/update_course_status', json=payload)

        assert response.status_code == 404
        assert response.json == {"message": "Invalid Course Id"}

    def test_update_course_status_without_course_id(self, client):
        payload = {}
        response = client.put('/api/update_course_status', json=payload)

        assert response.status_code == 404
        assert response.json == {"message": "course_id is required"}

    def test_admin_dashboard_success(self, client):
        response = client.get('/api/admin_dashboard')

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == 'dict'
        assert 'total_students' in json_data["data"]
        assert 'total_courses' in json_data["data"]
        assert 'active_courses' in json_data["data"]
        assert 'active_enrollments' in json_data["data"]
        assert type(json_data["data"]["total_students"]).__name__ == 'int'
        assert type(json_data["data"]["total_courses"]).__name__ == 'int'
        assert type(json_data["data"]["active_courses"]).__name__ == 'int'
        assert type(json_data["data"]["active_enrollments"]).__name__ == 'int'

    def test_get_user_name_success(self, client):
        response = client.get('/api/get_user_name/3')

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data['data']).__name__ == 'dict'
        assert "user_id" in json_data["data"]
        assert "name" in json_data["data"]
        assert "levels" in json_data["data"]
        assert type(json_data["data"]['user_id']).__name__ == 'int'
        assert type(json_data["data"]['name']).__name__ == 'str'
        assert type(json_data["data"]['levels']).__name__ == 'list'

    def test_get_user_name_invalid_id(self, client):
        response = client.get('/api/get_user_name/2')

        assert response.status_code == 404
        assert response.json == {"message": "Invalid User Id"}

    def test_course_recommender_success(self, client):
        payload = {
                        "user_id": 1,
                        "no_of_courses": 1,
                        "study_hour": 20,
                        "level": 1
                    }
        response = client.post('/api/course_recommender', json=payload)

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == 'list'
        assert len(json_data["data"]) == payload["no_of_courses"]
        assert "course_name" in json_data["data"][0]
        assert "estimated_marks" in json_data["data"][0]
        assert type(json_data["data"][0]["course_name"]).__name__ == 'str'
        assert type(json_data["data"][0]["estimated_marks"]).__name__ == 'float'

    def test_course_recommender_invalid_id(self, client):
        payload = {
                        "user_id": -1,
                        "no_of_courses": 1,
                        "study_hour": 20,
                        "level": 1
                    }
        response = client.post('/api/course_recommender', json=payload)

        assert response.status_code == 404
        assert response.json == {"message": "user_id is invalid"}

    def test_course_recommender_missing_user_id(self, client):
        payload = {
            "no_of_courses": 1,
            "study_hour": 20,
            "level": 1
        }
        response = client.post('/api/course_recommender', json=payload)

        assert response.status_code == 404
        assert response.json == {"message": "user_id is required"}


