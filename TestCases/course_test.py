# here is the file for creating course test cases
import pytest
import json
from main import app


class TestCourseCases:

    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    # ------------------------------------------ GET ------------------------------------------
    def test_getCourseSuccess(self, client):
        response = client.get('/api/course/1')

        assert response.status_code == 200
        assert response.json == {
                                        "data": {
                                            "code": "CS001214",
                                            "course_id": 1,
                                            "course_type": "Diploma in Programming",
                                            "description": "bla bla bla bla4",
                                            "duration": "12 weeks",
                                            "is_active": True,
                                            "level": "1",
                                            "name": "Java",
                                            "professor": "Someone"
                                        }
                                    }

    def test_getCourseFailure(self, client):
        response = client.get('api/course/-1')

        assert response.status_code == 404
        assert response.json == {"message": "Invalid Course id"}

    # ------------------------------------------ POST ------------------------------------------
    def test_postCourseFailure_course_code_already_taken(self, client):
        payload = {
            "code": "CS001214",
            "course_id": 2,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Python",
            "professor": "It is Me"
        }

        response = client.post('/api/course', json=payload)

        assert response.status_code == 400
        assert response.json == {"message": "Course Code is already taken"}

    def test_postCourseFailure_course_name_already_taken(self, client):
        payload = {
            "code": "CS001215",
            "course_id": 2,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Python",
            "professor": "It is Me"
        }

        response = client.post('/api/course', json=payload)

        assert response.status_code == 400
        assert response.json == {"message": "Course Name is already taken"}

    def test_postCourseSuccess(self, client):
        payload = {
            "code": "CS0012150",
            "course_id": 2,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Mathematical Thinking",
            "professor": "It is Me"
        }

        response = client.post('/api/course', json=payload)

        assert response.status_code == 201
        assert response.json == {"message": "Course Added Successfully"}

    # ------------------------------------------ PUT ------------------------------------------
    def test_putCourseFailure_invalid_course_code(self, client):
        payload = {
            "code": "CS001210",
            "course_id": -1,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Python",
            "professor": "It is Me"
        }

        response = client.put('/api/course/-1', json=payload)

        assert response.status_code == 404
        assert response.json == {"message": "Invalid Course id"}

    def test_putCourseFailure_course_code_already_taken(self, client):
        payload = {
            "code": "CS001214",
            "course_id": 4,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Python",
            "professor": "It is Me"
        }

        response = client.put('/api/course/4', json=payload)

        assert response.status_code == 400
        assert response.json == {"message": "Course Code is already taken"}

    def test_putCourseFailure_course_name_already_taken(self, client):
        payload = {
            "code": "CS001211",
            "course_id": 2,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "Python",
            "professor": "It is Me"
        }

        response = client.put('/api/course/2', json=payload)

        assert response.status_code == 400
        assert response.json == {"message": "Course Name is already taken"}

    def test_putCourseSuccess(self, client):
        payload = {
            "code": "CS123456",
            "course_id": 2,
            "course_type": "Diploma in Programming",
            "description": "Testing API POST",
            "duration": "8 weeks",
            "is_active": True,
            "level": "1",
            "name": "SE",
            "professor": "It is Ranjith"
        }

        response = client.put('/api/course/2', json=payload)

        assert response.status_code == 200
        assert response.json == {"message": "Course Updated Successfully"}

    # ------------------------------------------ DELETE ------------------------------------------
    def test_deleteCourseFailure_invalid_course_id(self, client):
        response = client.delete('/api/course/-1')

        assert response.status_code == 404
        assert response.json == {"message": "Invalid Course id"}

    def test_deleteCourseSuccess(self, client):
        response = client.delete('/api/course/7')

        assert response.status_code == 200
        assert response.json == {"message": "Course deleted Successfully"}

    # ------------------------------------------ USER COURSES ------------------------------------------
    def test_getUserCoursesSuccess(self, client):
        response = client.get('/api/courses/student/1')

        assert response.status_code == 200
        assert response.json["username"] == "M.Ikramm"
        assert len(response.json["Enrolled"]) == 1
        assert len(response.json["Unenrolled"]) == 4

    def test_getUserCoursesFailure(self, client):
        response = client.get('/api/courses/student/100')

        assert response.status_code == 404
        assert response.json == {"message": "user_id is invalid"}


