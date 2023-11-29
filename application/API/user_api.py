from main import app, db
from application.API.models import Users
from flask import request, make_response, jsonify
from flask_restful import Resource, Api
from application.API.additional_functions import validate_login_data, validate_signup_data, \
    validate_forget_password_data, validate_update_user_data

api = Api(app)


# -------------------------------Login API -------------------------------

@app.route("/api/login", methods=["POST"])
def login():
    """API Function for Login"""
    data = request.get_json()

    # Validating json data to ensure all required parameters are there and in correct order
    resp, status = validate_login_data(data)

    # If validation failed then passing response
    if not status:
        return resp

    # Checking for the user record
    user_recall = Users.query.filter_by(username=data["username"]).first()

    if user_recall:

        # Verifying password
        if user_recall.password == data["password"]:
            return make_response(jsonify({"message": "Login successful", "user_id": user_recall.user_id}), 200)

        else:
            return make_response(jsonify({"message": "Incorrect password!"}), 403)

    else:
        return make_response(jsonify({"message": "The Username you entered isn't connected to an account."}), 404)


# -------------------------------Sign Up API-------------------------------

@app.route("/api/signup", methods=["POST"])
def signup():
    """API Function for Sign Up"""
    data = request.get_json()

    # Validating the json data
    resp, status = validate_signup_data(data)

    # checking if data is validated else returning the error response
    if not status:
        return resp

    # Validating if given email already exists
    user_recall = Users.query.filter_by(email=data["email"]).first()

    if user_recall:
        return make_response(jsonify({"message": "The email address you entered is already connected to an account."}),
                             403)

    # Validating if given username already exists
    user_recall = Users.query.filter_by(username=data["username"]).first()

    if user_recall:
        return make_response(
            jsonify({"message": "The username you entered is already connected to an account."}),
            403)

    # Validating if given Roll number already exists
    user_recall = Users.query.filter_by(roll_no=data["roll_no"]).first()

    if user_recall:
        return make_response(
            jsonify({"message": "The roll_no you entered is already connected to an account."}),
            403)

    # Creating User object
    user_record = Users(email=data["email"], password=data["password"], name=data["name"], username=data["username"],
                        reset_code=data["reset_code"],
                        roll_no=data["roll_no"], dual_degree=data["dual_degree"], side_work=data["side_work"],
                        additional_education=data["additional_education"])
    try:
        # Adding the object and saving database
        db.session.add(user_record)
        db.session.commit()
        return make_response(jsonify({"message": "Account created successfully"}), 201)

    except:
        # Giving Error message in case of failure
        db.session.rollback()
        return make_response(jsonify({"message": "Something Went Wrong"}), 400)


# --------------------------------Forget Password API ------------------------------

@app.route("/api/forget_password", methods=["POST"])
def forget_password():
    """API Function for Forget Password"""

    data = request.get_json()
    # Validating the json data
    resp, status = validate_forget_password_data(data)

    # Returning Error Response message in case of validation failure
    if not status:
        return resp

    user_recall = Users.query.filter_by(username=data["username"]).first()

    # Verifying if account exists
    if user_recall:

        # Verifying given reset code and updating password
        if user_recall.reset_code == data["reset_code"]:
            user_recall.password = data["new_password"]
            # for saving the change
            try:
                db.session.commit()
                return make_response(jsonify({"message": "Password Reset Successfully"}), 202)

            except:
                db.session.rollback()
                return make_response(jsonify({"message": "Something went wrong"}), 500)

        else:
            return make_response(jsonify({"message": "The reset code you entered is incorrect."}), 403)

    else:
        return make_response(jsonify({"message": "Account doesn't exist"}), 404)


# ---------------- Approve Student API -----------------------------
@app.route("/api/student/approve", methods=["PUT"])
def approve_student():
    data = request.get_json()

    # Validating json data
    if "user_id" not in data:
        return make_response(jsonify({"message": "user_id is required"}), 404)

    if not isinstance(data["user_id"], int):
        return make_response(jsonify({"message": "user_id should be integer"}), 400)

    # Verifying the user_id
    user = Users.query.get(data["user_id"])
    if not user:
        return make_response(jsonify({"message": "invalid user_id"}), 404)

    try:
        # trying to make changes and save
        user.verified = True
        db.session.commit()
        return make_response(jsonify({"message": "User approved"}), 200)

    except:
        # reverting to last save in case of failure
        db.session.rollback()
        return make_response(jsonify({"message": "Something went wrong"}), 500)


# ---------------------- New Student List API ---------------------------
@app.route("/api/new_students", methods=["GET"])
def new_students():
    """API Functionality for getting new students list"""

    # Querying all new students
    students = Users.query.filter_by(verified=False).all()
    students_list = []
    for student in students:
        students_list.append(student.get_dictionary())

    return make_response(jsonify({"data": students_list}), 200)


# ------------------------------USER PROFILE RESTFUL APIs ------------------------------------

class ProfileAPI(Resource):
    @staticmethod
    def get(user_id):
        """API Function to get User record"""

        user_obj = Users.query.filter_by(user_id=user_id).first()
        if not user_obj:
            return make_response(jsonify({"message": "Invalid user_id"}), 404)
        return make_response(jsonify({"data": user_obj.get_dictionary()}), 200)


    @staticmethod
    def post():
        """API Function for creating user record"""

        data = request.get_json()

        # Validating json data
        resp, status = validate_signup_data(data)

        # In case of validation failure return appropriate error message response
        if not status:
            return resp

        # Verifying if given email already exists
        user_recall = Users.query.filter_by(email=data["email"]).first()
        if user_recall:
            return make_response(
                jsonify({"message": "The email address you entered is already connected to an account."}),
                403)

        # Validating if given username already exists
        user_recall = Users.query.filter_by(username=data["username"]).first()
        if user_recall:
            return make_response(
                jsonify({"message": "The username you entered is already connected to an account."}),
                403)

        # Validating if given Roll number already exists
        user_recall = Users.query.filter_by(roll_no=data["roll_no"]).first()
        if user_recall:
            return make_response(
                jsonify({"message": "The roll_no you entered is already connected to an account."}),
                403)

        # Creating User record
        user_record = Users(email=data["email"], password=data["password"], name=data["name"],
                            username=data["username"],
                            reset_code=data["reset_code"],
                            roll_no=data["roll_no"], dual_degree=data["dual_degree"], side_work=data["side_work"],
                            additional_education=data["additional_education"])

        try:
            # Adding the user record and saving database
            db.session.add(user_record)
            db.session.commit()
            return make_response(jsonify({"message": "Account created successfully"}), 201)

        except:
            # Rolling back database in case of failure to save
            db.session.rollback()
            return make_response(jsonify({"message": "Something Went Wrong"}), 400)

    @staticmethod
    def put(user_id):
        """API Function for Updating User record"""

        data = request.get_json()

        # Validating json data
        resp, status = validate_update_user_data(data)

        # If validation fails then passing the appropriate response
        if not status:
            return resp

        edit_profile_obj = Users.query.filter_by(user_id=user_id).first()

        # Verifying that user_id is valid and it belongs to the same username for updating
        if not edit_profile_obj or edit_profile_obj.username != data["username"]:
            return make_response(jsonify({"message": "Invalid User Id"}), 400)

        # Verifying if email already exist in database attached to some other account
        record = Users.query.filter_by(email=data["email"]).first()

        if record and record.username != edit_profile_obj.username:
            return make_response(jsonify({"message": "Email is already taken, please try another"}), 400)

        (
            edit_profile_obj.name,
            edit_profile_obj.email,
            edit_profile_obj.password,
            edit_profile_obj.reset_code,
            edit_profile_obj.dual_degree,
            edit_profile_obj.side_work,
            edit_profile_obj.additional_education
        ) = (
            data["name"],
            data["email"],
            data["password"],
            data["reset_code"],
            data["dual_degree"],
            data["side_work"],
            data["additional_education"]
        )

        try:
            # Saving changes to database
            db.session.commit()
            return make_response(jsonify({"message": "Profile updated successfully"}), 202)
        except:
            # Rolling back in case of failure to save
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)


api.add_resource(ProfileAPI, "/api/profile/<user_id>", "/api/profile")

from application.API.course_api import *
from application.API.review_api import *
from application.API.enrollment_api import *
from application.API.other_api import *
