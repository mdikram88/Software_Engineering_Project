from main import app, db
from flask import request, make_response, jsonify
from flask_restful import Resource
from application.API.models import *
from application.API.additional_functions import validate_review_data, validate_update_review_data

from application.API.user_api import api


class ReviewsAPI(Resource):
    @staticmethod
    def get(review_id):
        """API Function to get Review data"""

        # Verifying if review_id is valid
        review = Reviews.query.get(review_id)

        if review:
            d = review.get_dictionary()
            d["course_name"] = review.course.name
            return make_response(jsonify({"data": d}), 200)
        return make_response(jsonify({"message": "Invalid review_id"}), 404)

    @staticmethod
    def post():
        """API Function for adding review"""

        data = request.get_json()

        # Validating json data
        resp, status = validate_review_data(data)

        # If validation failed, then passing appropriate message
        if not status:
            return resp

        # Verifying user id
        user = Users.query.get(data["user_id"])
        if not user:
            return make_response(jsonify({"message": "Invalid user_id"}), 404)

        # Verifying course id
        course = Courses.query.get(data["course_id"])
        if not course:
            return make_response(jsonify({"message": "Invalid course_id"}), 404)

        # Verifying if student has enrolled in the given course
        enrollment = Enrollments.query.filter_by(user_id=data["user_id"], course_id=data["course_id"]).first()
        if not enrollment:
            return make_response(jsonify({"message": "User has not enrolled for this course"}), 400)

        # Verifying if user has given review to this course before or not
        record = Reviews.query.filter_by(user_id=data["user_id"], course_id=data["course_id"]).first()
        if record:
            return make_response(jsonify({"message": "Can't give more than one review for each course"}), 400)

        # Creating review object
        review = Reviews(review=data["review"], difficulty=data["difficulty"], support=data["support"],
                         rating=data["rating"], user_id=data["user_id"], course_id=data["course_id"])

        try:
            # Trying to add review and save database
            db.session.add(review)
            db.session.commit()
            return make_response(jsonify({"message": "Review Added Successfully"}), 201)

        except:
            # In case of failure , rolling back database
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong!"}), 500)

    @staticmethod
    def put():
        """API Function for updating review data"""

        data = request.get_json()

        # Validating the json data
        resp, status = validate_update_review_data(data)

        # In case of validation failure, passing appropriate response
        if not status:
            return resp

        # verifying if review_id is valid
        review = Reviews.query.get(data["review_id"])
        if not review:
            return make_response(jsonify({"message": "Invalid Review Id"}), 404)

        # Updating Review data
        review.review = data["review"]
        review.difficulty = data["difficulty"]
        review.support = data["support"]
        review.rating = data["rating"]

        try:
            db.session.commit()
            return make_response(jsonify({"message": "Review Successfully Updated"}), 202)
        except:
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)

    @staticmethod
    def delete(review_id):
        """API Function for deleting Review"""

        data = request.get_json()

        # Verifying if review_id is valid
        review = Reviews.query.get(data["review_id"])
        if not review:
            return make_response(jsonify({"message": "Invalid Review Id"}), 404)

        try:
            # trying to delete review and save database
            db.session.delete(review)
            db.session.commit()
            return make_response(jsonify({"message": "Review Deleted Successfully"}), 200)

        except:
            # in case of failure, rolling back database to last save
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong"}), 500)


@app.route("/api/reviews/student/<int:user_id>", methods=["GET"])
def student_reviews(user_id):
    """API Function to get reviews given by the particular user"""

    # Verifying if user_id is valid in database
    user = Users.query.get(user_id)
    if not user:
        return make_response(jsonify({"message": "Invalid user_id"}), 404)

    # Create review list of dictionaries given by the particular user
    review_list = []
    for review in user.reviews:
        d = review.get_dictionary()
        d["course_name"] = review.course.name
        review_list.append(d)

    return make_response(jsonify({"data": review_list}), 200)


api.add_resource(ReviewsAPI, "/api/review", "/api/review/<int:review_id>")
