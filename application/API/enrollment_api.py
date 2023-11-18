from main import app, db
from flask import request, make_response, jsonify
from flask_restful import Resource
from application.API.models import *
from application.API.additional_functions_2 import validate_enroll_data, validate_update_enroll_data
from application.API.user_api import api


# ------------------------- Student's Enrollment list API -------------------
@app.route("/api/enrollments/student/<int:user_id>", methods=["GET"])
def student_enrollments(user_id):
    """API Function for getting enrollment list of particular user"""

    user = Users.query.get(user_id)
    if not user:
        return make_response(jsonify({"message": "user_id is invalid"}), 404)

    enrollments = []

    for enroll in user.enrollments:
        enrollments.append(enroll.get_dictionary())

    return make_response(jsonify({"data": enrollments}), 200)


# ------------------------- All Enrollment List API ------------------
@app.route("/api/enrollments/admin", methods=["GET"])
def all_enrollments():
    enrollments = Enrollments.query.all()
    enrollments_list = []

    for enrollment in enrollments:
        enrollments_list.append(enrollment.get_dictionary())

    return make_response(jsonify({"data": enrollments_list}), 200)


# ------------------------------RESTful Enrollment API -------------------------
class EnrollmentAPI(Resource):
    @staticmethod
    def get(enroll_id):
        """API Function for getting enrollment data"""

        # Verifying if enrollment id is valid
        enrollment = Enrollments.query.get(enroll_id)
        if not enrollment:
            return make_response(jsonify({"message": "Enrollment id is invalid"}), 404)

        return make_response(jsonify({"data": enrollment.get_dictionary()}), 200)

    @staticmethod
    def post():
        """API Function for adding enrollment data"""

        data = request.get_json()

        # Validating json data
        resp, status = validate_enroll_data(data)

        # In case of failure, passing appropriate data
        if not status:
            return resp

        # Verifying user_id
        user = Users.query.get(data["user_id"])
        if not user:
            return make_response(jsonify({"message": "Invalid user id"}), 404)

        if not user.verified:
            return make_response(jsonify({"message": "User is not verified"}), 400)

        # Verifying course_id
        course = Courses.query.get(data["course_id"])
        if not course:
            return make_response(jsonify({"message": "Invalid course_id"}), 404)

        # Verifying if enrollment already exist
        enroll = Enrollments.query.filter_by(user_id=data["user_id"], course_id=data["course_id"]).first()
        if enroll:
            return make_response(jsonify({"message": "Enrollment already exist for this user and course"}), 400)

        # Creating Enrollment record
        enrollment = Enrollments(course_id=data["course_id"], user_id=data["user_id"], marks=data["marks"],
                                 term=data["term"], year=data["year"], study_hours=data["study_hours"])

        try:
            # Trying to add enrollment and save database
            db.session.add(enrollment)
            db.session.commit()
            return make_response(jsonify({"message": "Enrollment Added Successfully"}), 201)

        except:
            # In case of failure, rolling back
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)

    @staticmethod
    def put(enroll_id):
        """API Function for updating enrollment data"""

        data = request.get_json()
        resp, status = validate_update_enroll_data(data)

        if not status:
            return resp

        # Verifying enrollment exists
        enrollment = Enrollments.query.get(enroll_id)
        if not enrollment:
            return make_response(jsonify({"message": "Enrollment id is invalid"}), 404)

        enrollment.marks = data["marks"]
        enrollment.term = data["term"]
        enrollment.year = data["year"]
        enrollment.study_hours = data["study_hours"]

        try:
            # Trying to save the changes
            db.session.commit()
            return make_response(jsonify({"message": "Enrollment Updated Successfully"}), 202)

        except:
            # In case of failure, rolling back
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)

    @staticmethod
    def delete(enroll_id):
        """API Function for deleting Enrollment"""

        enrollment = Enrollments.query.get(enroll_id)
        if not enrollment:
            return make_response(jsonify({"message": "enrollment id is invalid"}), 404)

        try:
            # Trying to delete enrollment and saving database
            db.session.delete(enrollment)
            db.session.commit()
            return make_response(jsonify({"message": "Enrollment deleted Successfully"}), 200)

        except:
            # In case of failure, rolling back to last save
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)


api.add_resource(EnrollmentAPI, "/api/enrollments", "/api/enrollments/<int:enroll_id>")

