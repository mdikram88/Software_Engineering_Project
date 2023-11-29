# here is the file for creating enrollment test cases
import pytest
import json

from werkzeug.wrappers import response
from main import app


class TestEnrollmentCases:

    # general cases
    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    def test_get_enrollment_student(self, client):
        response = client.get('api/enrollments/student/1')
        assert response.status_code == 200
        assert "data" in response.json

    def test_get_enrollment_student_not_found(self, client):
        response = client.get('api/enrollments/student/1000')
        assert response.status_code == 404
        assert response.json == {"message": "user_id is invalid"}

    def test_all_enrollment(self, client):
        response = client.get('api/enrollments/admin')
        assert response.status_code == 200
        assert "data" in response.json
        assert type(response.json["data"]).__name__ == 'list'

    # put cases
    def test_put_enrollment_id_failure(self, client):

        response = client.put('api/enrollments/600')
        assert response.status_code == 404
        assert response.json == {"message": "Enrollment id is invalid"}

    def test_put_enrollment_id_success(self, client):
        payload = {
                        "marks": 70,
                        "term": "Sept",
                        "year": 2022,
                        "study_hours": 30
                    }
        response = client.put('api/enrollments/5', json=payload)
        assert response.status_code == 202
        assert response.json == {"message": "Enrollment Updated Successfully"}


    # post cases
    def test_post_enrollment_case_1(self, client):
        payload = {
                    "course_id": 2,
                    "user_id": -1,
                    "marks": 70,
                    "term": "Sept",
                    "year": 2022,
                    "study_hours": 20
                }
        response = client.post('/api/enrollments', json=payload)
        assert response.status_code == 404
        assert response.json == {"message": "Invalid user id"}

    def test_post_enrollment_case_2(self, client):
        payload = {
                        "course_id": 2,
                        "user_id": 6,
                        "marks": 70,
                        "term": "Sept",
                        "year": 2022,
                        "study_hours": 20
                    }
        response = client.post('/api/enrollments', json=payload)
        assert response.status_code == 400
        assert response.json == {"message": "User is not verified"}

    def test_post_enrollment_case_3(self, client):
        payload = {
                        "course_id": 200,
                        "user_id": 3,
                        "marks": 70,
                        "term": "Sept",
                        "year": 2022,
                        "study_hours": 20
                    }
        response = client.post('/api/enrollments', json=payload)
        assert response.status_code == 404
        assert response.json == {"message": "Invalid course_id"}

    def test_post_enrollment_case_4(self, client):
        payload = {
                        "course_id": 2,
                        "user_id": 3,
                        "marks": 70,
                        "term": "Sept",
                        "year": 2022,
                        "study_hours": 20
                    }
        response = client.post('/api/enrollments', json=payload)
        assert response.status_code == 400
        assert response.json == {"message": "Enrollment already exist for this user and course"}

    def test_post_enrollment_case_5(self, client):
        payload = {"course_id": 1, "user_id": 3, "marks": 100, "term": "Sept", "year": 2023, "study_hours": 40}
        response = client.post('/api/enrollments', json=payload)
        assert response.status_code == 201
        assert response.json == {"message": "Enrollment Added Successfully"}


    # delete cases
    def test_delete_enrollment_id_failure(self, client):
        response = client.delete('api/enrollments/600')
        assert response.status_code == 404
        assert response.json == {"message": "enrollment id is invalid"}

    def test_delete_enrollment_id_success(self, client):
        response = client.delete('/api/enrollments/6')
        assert response.status_code == 200
        assert response.json == {"message": "Enrollment deleted Successfully"}


