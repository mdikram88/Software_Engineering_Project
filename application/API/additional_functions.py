from flask import make_response, jsonify
import re


def is_valid_email(email):
    """Function to validate email pattern"""

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Use re.match() to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    return False


def is_valid_name(name):
    """Function to validate name pattern"""
    # Define a regular expression pattern for a name with only alphabets and white spaces
    pattern = r'^[a-zA-Z\s.]+$'

    # Use re.match() to check if the name matches the pattern
    if re.match(pattern, name):
        return True

    return False


def validate_login_data(data):
    """Function to validate the login json object"""

    if "username" not in data:
        return make_response(jsonify({"message": "'username' is required"}), 404), False

    if not data["username"].isalnum():
        return make_response(jsonify({"message": "Invalid username format, Only Alphanumeric is allowed"}), 400), False

    if "password" not in data:
        return make_response(jsonify({"message": "'password' is required"}), 404), False

    if len(data["password"]) < 8:
        return make_response(jsonify({"message": "'password' should be atleast 8 characters"}), 400), False

    return None, True


def validate_signup_data(data):
    """Function to validate Sign Up json data"""

    if "roll_no" not in data:
        return make_response(jsonify({"message": "'roll_no' is required"}), 404), False

    resp, status = validate_update_user_data(data)
    if not status:
        return resp, status

    return None, True


def validate_forget_password_data(data):
    """Function to validate the forget password data"""

    if "username" not in data:
        return make_response(jsonify({"message": "'username' is required"}), 404), False

    if not data["username"].isalnum():
        return make_response(jsonify({"message": "Invalid username format, Only Alphanumeric is allowed"}), 400), False

    if "new_password" not in data:
        return make_response(jsonify({"message": "'new_password' is required"}), 404), False

    if len(data["new_password"]) < 8:
        return make_response(jsonify({"message": "'new_password' should be atleast 8 characters"}), 400), False

    if "reset_code" not in data:
        return make_response(jsonify({"message": "'reset_code' is required"}), 404), False

    if len(data["reset_code"]) < 6:
        return make_response(jsonify({"message": "reset_code should be atleast 6 characters"}), 400), False

    return None, True


def validate_update_user_data(data):
    """Function to validate update user data"""

    if "email" not in data:
        return make_response(jsonify({"message": "'email' is required"}), 404), False

    if not is_valid_email(data["email"]):
        return make_response(jsonify({"message": "Invalid email format"}), 400), False

    if "password" not in data:
        return make_response(jsonify({"message": "'password' is required"}), 404), False

    if len(data["password"]) < 8:
        return make_response(jsonify({"message": "password should be atleast 8 characters"}), 400), False

    if "name" not in data:
        return make_response(jsonify({"message": "'name' is required"}), 404), False

    if not is_valid_name(data["name"]):
        return make_response(jsonify({"message": "No special characters or numbers are allowed in name"}), 400), False

    if "username" not in data:
        return make_response(jsonify({"message": "'username' is required"}), 404), False

    if not data["username"].isalnum():
        return make_response(jsonify({"message": "Invalid username format, Only Alphanumeric is allowed"}), 400), False

    if "reset_code" not in data:
        return make_response(jsonify({"message": "'reset_code' is required"}), 404), False

    if len(data["reset_code"]) < 6:
        return make_response(jsonify({"message": "reset_code should be atleast 6 characters"}), 400), False

    if "dual_degree" not in data:
        return make_response(jsonify({"message": "'dual_degree' is required"}), 404), False

    if type(data["dual_degree"]).__name__ != 'bool':
        return make_response(jsonify({"message": "'dual_degree' is required to be boolean only"}), 400), False

    if "side_work" not in data:
        return make_response(jsonify({"message": "'side_work' is required"}), 404), False

    if type(data["side_work"]).__name__ != 'bool':
        return make_response(jsonify({"message": "'side_work' is required to be boolean only"}), 400), False

    if "additional_education" not in data:
        return make_response(jsonify({"message": "'additional_education' is required"}), 404), False

    return None, True


def validate_course_data(data):
    """Function to validate course data"""

    if "code" not in data:
        return make_response(jsonify({"message": "'code' is required"}), 404), False

    if len(data["code"].strip()) == 1:
        return make_response(jsonify({"message": "'code' cannot be empty"}), 400), False

    if "name" not in data:
        return make_response(jsonify({"message": "'name' is required"}), 404), False

    if not is_valid_name(data["name"]):
        return make_response(jsonify({"message": "No special characters or numbers are allowed in name"}), 403), False

    if "description" not in data:
        return make_response(jsonify({"message": "'description' is required"}), 404), False

    if "professor" not in data:
        return make_response(jsonify({"message": "'professor' is required"}), 404), False

    if not is_valid_name(data["professor"]):
        return make_response(jsonify({"message": "No special characters or numbers are allowed in professor"}),
                             403), False

    if "course_type" not in data:
        return make_response(jsonify({"message": "'course_type' is required"}), 404), False

    if "duration" not in data:
        return make_response(jsonify({"message": "'duration' is required"}), 404), False

    if "level" not in data:
        return make_response(jsonify({"message": "'level' is required"}), 404), False

    return None, True


def validate_review_data(data):
    """Function to validate review data"""

    if "user_id" not in data:
        return make_response(jsonify({"message": "user_id is required"}), 404), False

    if not isinstance(data["user_id"], int):
        return make_response(jsonify({"message": "user_id should be integer"}), 400), False

    if "course_id" not in data:
        return make_response(jsonify({"message": "course_id is required"}), 404), False

    if not isinstance(data["course_id"], int):
        return make_response(jsonify({"message": "course_id should be integer"}), 400), False

    if "difficulty" not in data:
        return make_response(jsonify({"message": "difficulty is required"}), 404), False

    if not isinstance(data["difficulty"], int):
        return make_response(jsonify({"message": "difficulty value should be integer"}), 400), False

    if "rating" not in data:
        return make_response(jsonify({"message": "rating is required"}), 404), False

    if not isinstance(data["rating"], int):
        return make_response(jsonify({"message": "rating value should be integer"}), 400), False

    if "support" not in data:
        return make_response(jsonify({"message": "support is required"}), 404), False

    if not isinstance(data["support"], int):
        return make_response(jsonify({"message": "support value should be integer"}), 400), False

    if "review" not in data:
        return make_response(jsonify({"message": "review is required"}), 404), False

    return None, True


def validate_update_review_data(data):
    """Function to validate update review data"""

    if "review_id" not in data:
        return make_response(jsonify({"message": "review_id is required"}), 404), False

    if not isinstance(data["review_id"], int):
        return make_response(jsonify({"message": "review_id should be integer"}), 400), False

    if "difficulty" not in data:
        return make_response(jsonify({"message": "difficulty is required"}), 404), False

    if not isinstance(data["difficulty"], int):
        return make_response(jsonify({"message": "difficulty value should be integer"}), 400), False

    if "rating" not in data:
        return make_response(jsonify({"message": "rating is required"}), 404), False

    if not isinstance(data["rating"], int):
        return make_response(jsonify({"message": "rating value should be integer"}), 400), False

    if "support" not in data:
        return make_response(jsonify({"message": "support is required"}), 404), False

    if not isinstance(data["support"], int):
        return make_response(jsonify({"message": "support value should be integer"}), 400), False

    if "review" not in data:
        return make_response(jsonify({"message": "review is required"}), 404), False

    return None, True


def get_review_details(course):
    """Function to get review details of given course"""

    d = {}
    d["avg_rating"] = 0
    d["avg_difficulty"] = 0
    d["support"] = 0
    l = len(course.reviews)

    if l > 0:
        rating = 0
        difficulty = 0
        support = 0

        for review in course.reviews:
            rating += review.rating
            difficulty += review.difficulty
            support += review.support

        d["avg_rating"] = rating / l
        d["avg_difficulty"] = difficulty / l
        d["support"] = support / l
    return d


def get_course_details(course):
    """Function to get course details of given course"""

    d = course.get_dictionary()

    # getting review details of the course
    dt = get_review_details(course)

    if dt["avg_rating"] == 0:
        d["avg_rating"] = "Nil"
    else:
        d["avg_rating"] = dt["avg_rating"]

    if dt["avg_difficulty"] == 0:
        d["avg_difficulty"] = "Nil"
    else:
        d["avg_difficulty"] = dt["avg_difficulty"]

    if dt["support"] == 0:
        d["support"] = "Nil"
    else:
        d["support"] = dt["support"]

    return d


def get_enrolled_courses(student, only_ids=False):
    """Function to get enrolled courses data"""

    if not only_ids:
        enrolled_courses = []
        for enrollment in student.enrollments:
            enrolled_courses.append(enrollment.enroll_course.get_dictionary())

        return enrolled_courses
    else:
        enrolled_courses_id = []
        for enrollment in student.enrollments:
            enrolled_courses_id.append(enrollment.enroll_course.course_id)

        return enrolled_courses_id


def get_unenrolled_courses(student, courses):
    """Function to get unenrolled course data"""

    enrolled_course_ids = get_enrolled_courses(student, only_ids=True)
    unenrolled_courses = []
    for course in courses:
        if course.course_id not in enrolled_course_ids:
            unenrolled_courses.append(course.get_dictionary())

    return unenrolled_courses


