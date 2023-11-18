from main import app, db
from flask import request, make_response, jsonify
from flask_restful import Resource
from application.API.models import *
from application.API.additional_functions import get_enrolled_courses, \
    get_unenrolled_courses, validate_course_data

from application.API.user_api import api


# -------------------------Student Course API------------------------------

@app.route("/api/courses/student", methods=["POST"])
def student_courses():
    data = request.get_json()
    student = Users.query.get(data["user_id"])
    if data["enrollment_type"].lower() == "enrolled":
        enrolled_courses = get_enrolled_courses(student)
        return make_response(jsonify({"data": enrolled_courses}), 200)

    elif data["enrollment_type"].lower() == "unenrolled":
        courses = Courses.query.all()
        unenrolled_courses = get_unenrolled_courses(student, courses)

        return make_response(jsonify({"data": unenrolled_courses}), 200)
    else:
        return make_response(jsonify({"message": "Invalid enrollment_type"}), 400)


# -------------------------------Student Courses List API ---------------------------

@app.route("/api/courses/student/<user_id>", methods=["GET"])
def course_list(user_id):
    """API Function for getting student courses list"""

    user = Users.query.get(user_id)
    if not user:
        return make_response(jsonify({"message": "user_id is invalid"}), 404)

    user_enrollments = Enrollments.query.filter_by(user_id=user_id).all()
    enrolled_courses = []
    for enroll in user_enrollments:
        course = Courses.query.filter_by(course_id=enroll.course_id).first()
        enrolled_courses.append(course)

    Unenrolled_courses = Courses.query.filter(Courses.course_id.not_in([i.course_id for i in enrolled_courses])).all()
    user_obj = Users.query.filter_by(user_id=user_id).first()

    # reviews_enrolled_courses = [Reviews.query.filter_by(course_id = i.course_id).first() for i in enrolled_courses]
    # reviews_unenrolled_courses = [Reviews.query.filter_by(course_id = i.course_id).first() for i in Unenrolled_courses]

    enrolled_courses_data = []
    for i in enrolled_courses:
        courses_reviews = Reviews.query.filter_by(course_id=i.course_id).all()
        enrolled_courses_rating = [i.rating for i in courses_reviews]
        enrolled_courses_difficulty = [i.difficulty for i in courses_reviews]

        avg_enrolled_courses_rating = sum(enrolled_courses_rating) / len(enrolled_courses_rating) if len(
            enrolled_courses_rating) != 0 else 0
        avg_enrolled_courses_difficulty = sum(enrolled_courses_difficulty) / len(enrolled_courses_difficulty) if len(
            enrolled_courses_difficulty) != 0 else 0

        enrolled_courses_data.append(
            (i.code, i.duration, i.professor, avg_enrolled_courses_rating, avg_enrolled_courses_difficulty, i.course_id,
             i.name)
        )

    Unenrolled_courses_data = []
    for i in Unenrolled_courses:
        courses_reviews = Reviews.query.filter_by(course_id=i.course_id).all()
        Unenrolled_courses_rating = [i.rating for i in courses_reviews]
        Unenrolled_courses_difficulty = [i.difficulty for i in courses_reviews]

        avg_Unenrolled_courses_rating = sum(Unenrolled_courses_rating) / len(Unenrolled_courses_rating) if len(
            Unenrolled_courses_rating) != 0 else 0
        avg_Unenrolled_courses_difficulty = sum(Unenrolled_courses_difficulty) / len(
            Unenrolled_courses_difficulty) if len(Unenrolled_courses_difficulty) != 0 else 0

        Unenrolled_courses_data.append(
            (i.code, i.duration, i.professor, avg_Unenrolled_courses_rating, avg_Unenrolled_courses_difficulty,
             i.course_id, i.name)
        )

    data = {
        "username": user_obj.name,
        "Enrolled": enrolled_courses_data,
        "Unenrolled": Unenrolled_courses_data,
    }
    return data, 200


#  -----------------------------Course RESTful APIs ----------------------------------

class CourseAPI(Resource):
    @staticmethod
    def get(course_id):
        """API Function for getting particular course data"""

        course_obj = Courses.query.filter_by(course_id=course_id).first()
        if course_obj:
            return make_response(jsonify({"data": course_obj.get_dictionary()}), 200)
        return make_response(jsonify({"message": "Invalid Course id"}), 404)

    @staticmethod
    def post():
        """API Function for Adding Course"""

        data = request.get_json()

        # Validating json data
        resp, status = validate_course_data(data)

        # If validation failed then passing appropriate message
        if not status:
            return resp

        # Verifying if the course code is unique
        course_record = Courses.query.filter_by(code=data["code"]).first()
        if course_record:
            return make_response(jsonify({"message": "Course Code is already taken"}), 400)

        # Verifying if the course name is unique
        course_record = Courses.query.filter_by(name=data["name"]).first()
        if course_record:
            return make_response(jsonify({"message": "Course Name is already taken"}), 400)

        # Creating new Course object
        course_obj = Courses(
            code=data["code"],
            name=data["name"],
            description=data["description"],
            professor=data["professor"],
            course_type=data["course_type"],
            duration=data["duration"],
            level=data["level"]
        )

        try:
            # Trying to add course and save database
            db.session.add(course_obj)
            db.session.commit()
            return make_response(jsonify({"message": "Course Added Successfully"}), 201)

        except:
            # Rolling back in case of failure to save
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)

    @staticmethod
    def put(course_id):
        """API Function to update course"""

        data = request.get_json()

        course_obj = Courses.query.filter_by(course_id=course_id).first()

        # Checking if the course id is valid
        if not course_obj:
            return make_response(jsonify({"message": "Invalid Course id"}), 404)

        # Validating json data
        resp, status = validate_course_data(data)

        # If validation failed then passing appropriate message
        if not status:
            return resp

        # Verifying if the course code is unique
        course_record = Courses.query.filter_by(code=data["code"]).first()
        if course_record and course_record.course_id != course_obj.course_id:
            return make_response(jsonify({"message": "Course Code is already taken"}), 400)

        # Verifying if the course name is unique
        course_record = Courses.query.filter_by(name=data["name"]).first()
        if course_record and course_record.course_id != course_obj.course_id:
            return make_response(jsonify({"message": "Course Name is already taken"}), 400)

        (
            course_obj.name,
            course_obj.code,
            course_obj.duration,
            course_obj.professor,
            course_obj.course_type,
            course_obj.level,
            course_obj.description

        ) = (
            data["name"],
            data["code"],
            data["duration"],
            data["professor"],
            data["course_type"],
            data["level"],
            data["description"]

        )
        try:
            # Trying to save changes in database
            db.session.commit()
            return make_response(jsonify({"message": "Course Updated Successfully"}), 200)

        except:
            # In case of failure rolling back database to last save
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)

    @staticmethod
    def delete(course_id):
        """API Function for deleting course"""

        course_obj = Courses.query.filter_by(course_id=course_id).first()

        if course_obj:
            try:
                # trying to delete and save database
                db.session.delete(course_obj)
                db.session.commit()
                return make_response(jsonify({"message": "Course deleted Successfully"}), 200)
            except:
                # Rolling back in case of failure
                db.session.rollback()
                return make_response(jsonify({"message": "Something went wrong"}), 500)

        return make_response(jsonify({"message": "Invalid Course id"}), 404)


api.add_resource(CourseAPI, '/api/course', '/api/course/<course_id>')
