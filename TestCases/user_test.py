import json
import pytest
from main import app


# here is the file for creating user test cases


class Testcase1:

    @pytest.fixture
    def client(self):
        # Use the test client provided by pytest-flask
        return app.test_client()

    # Pytest cases for LOGIN API

    # login api - username not in DB
    def test_login_wrong_username(self, client):
        # Simulate a GET request to the '/' route
        payload = {
            "username": "testuser",
            "password": "test12345678"
        }
        response = client.post('/api/login', json=payload)

        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "The Username you entered isn't connected to an account."
        }

    # login api - correct login credentials
    def test_login_correct_credentials(self, client):
        payload = {
            "username": "mdikram888",
            "password": "12345678"
        }
        response = client.post('/api/login', json=payload)
        # Check that the response is as expected
        assert response.status_code == 200
        assert response.json == {
            "message": "Login successful",
            "user_id": 7
        }

    # login api - password not given
    def test_login_password_required(self, client):
        payload = {
            "username": "mdikram888",

        }
        response = client.post('/api/login', json=payload)
        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "'password' is required"
        }

    # login api - password not given
    def test_login_password_length(self, client):
        payload = {
            "username": "mdikram888",
            "password": "123456"
        }
        response = client.post('/api/login', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {
            "message": "'password' should be atleast 8 characters"
        }

    # Pytest cases for SIGNUP API

    # signup api - correct signup details
    def test_correct_signup(self, client):
        payload = {
            "username": "username4",
            "email": "stone388019@gmail.com",
            "password": "acdb1234",
            "roll_no": "23f1005524",
            "name": "bimleshkanth",
            "reset_code": "202001",
            "dual_degree": False,
            "side_work": False,
            "additional_education": "PhD"
        }
        response = client.post('/api/signup', json=payload)
        # Check that the response is as expected
        assert response.status_code == 201
        assert response.json == {
            "message": "Account created successfully"
        }

    # signup api - missing roll no
    def test_signup_missing_rollno(self, client):
        payload = {
            "username": "username4",
            "email": "stone388019@gmail.com",
            "password": "acdb1234",

            "name": "bimleshkanth",
            "reset_code": "202001",
            "dual_degree": False,
            "side_work": False,
            "additional_education": "PhD"
        }
        response = client.post('/api/signup', json=payload)
        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "'roll_no' is required"
        }

    # Pytest cases for FORGET PASSWORD API

    # password api - correct password details
    def test_correct_pwd_reset(self, client):
        payload = {
            "username": "username4",
            "new_password": "newpwd1234",
            "reset_code": "202001",
        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 202
        assert response.json == {
            "message": "Password Reset Successfully"
        }

    # password api - no username passed
    def test_pwd_reset_no_username(self, client):
        payload = {

            "new_password": "newpwd1234",
            "reset_code": "202001",
        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "'username' is required"
        }

    # password api - no alphanumeric username passed
    def test_pwd_reset_no_alphanumeric_username(self, client):
        payload = {
            "username": "username4@#",
            "new_password": "newpwd1234",
            "reset_code": "202001",
        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {
            "message": "Invalid username format, Only Alphanumeric is allowed"
        }

    # password api - no new password passed
    def test_pwd_reset_no_new_password(self, client):
        payload = {
            "username": "username4",

            "reset_code": "202001"
        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "'new_password' is required"
        }

    # password api - new password length short
    def test_pwd_reset_new_password_short(self, client):
        payload = {
            "username": "username4",
            "new_password": "1234",
            "reset_code": "202001"
        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {
            "message": "'new_password' should be atleast 8 characters"
        }

    # password api - no reset code passed
    def test_pwd_reset_new_password_no_reset_code(self, client):
        payload = {
            "username": "username4",
            "new_password": "newpwd1234"

        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 404
        assert response.json == {
            "message": "'reset_code' is required"
        }

    # password api - reset code short
    def test_pwd_reset_new_password_reset_code_short(self, client):
        payload = {
            "username": "username4",
            "new_password": "newpwd1234",
            "reset_code": "2021"

        }
        response = client.post('/api/forget_password', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {
            "message": "reset_code should be atleast 6 characters"
        }

    # Pytest cases for UPDATE USER DATA API

    # update user data api -
    def test_correct_update_user(self, client):
        payload = {

            "email": "stone388019@gmail.com",
            "password": "acdbe1234",
            "username": "username4",
            "name": "bimleshkanth",
            "reset_code": "202001",
            "dual_degree": False,
            "side_work": False,
            "additional_education": "PhD"
        }
        response = client.put('/api/profile/8', json=payload)
        # Check that the response is as expected
        assert response.status_code == 202
        assert response.json == {
            "message": "Profile updated successfully"
        }

    # update user data api - wrong user_id username combination
    def test_update_user_wrong_useridUsername(self, client):
        payload = {

            "email": "stone388019@gmail.com",
            "password": "acdbe1234",
            "username": "username4",
            "name": "bimleshkanth",
            "reset_code": "202001",
            "dual_degree": False,
            "side_work": False,
            "additional_education": "PhD"
        }
        response = client.put('/api/profile/7', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {"message": "Invalid User Id"}

    # update user data api - wrong user_id username combination
    def test_update_user_email_existing(self, client):
        payload = {

            "email": "game388019@gmail.com",
            "password": "acdbe1234",
            "username": "username4",
            "name": "bimleshkanth",
            "reset_code": "202001",
            "dual_degree": False,
            "side_work": False,
            "additional_education": "PhD"
        }
        response = client.put('/api/profile/8', json=payload)
        # Check that the response is as expected
        assert response.status_code == 400
        assert response.json == {"message": "Email is already taken, please try another"}

    def test_user_view_success(self, client):
        response = client.get('/api/profile/1')

        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == "dict"
        assert "username" in json_data["data"]

    def test_user_view_failed_invalid_id(self, client):
        response = client.get('/api/profile/2')

        assert response.status_code == 404
        assert response.json == {
                                    "message": "Invalid user_id"
                                }


    def test_approve_student_success(self, client):
        payload = {"user_id": 1}
        response = client.put('/api/student/approve', json=payload)
        assert response.status_code == 200
        assert response.json == {"message": "User approved"}

    def test_approve_student__failed_string_user_id(self, client):
        payload = {"user_id":"1"}
        response = client.put('/api/student/approve', json=payload)
        assert response.status_code == 400
        assert response.json == {"message": "user_id should be integer"}

    def test_approve_student_failed_invalid_id(self, client):
        payload = {"user_id": -1}
        response = client.put('/api/student/approve', json=payload)
        assert response.status_code == 404
        assert response.json == {"message": "invalid user_id"}

    def test_all_students_success(self, client):
        response = client.get("/api/new_students")
        json_data = response.json
        assert response.status_code == 200
        assert "data" in json_data
        assert type(json_data["data"]).__name__ == 'list'
        if len(json_data["data"]) > 0:
            assert type(json_data["data"][0]).__name__ == 'dict'
