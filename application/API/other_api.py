from main import app, db
from apscheduler.schedulers.background import BackgroundScheduler
from flask import make_response, jsonify, request, send_file
from application.API.models import *
from application.API.additional_functions_2 import create_pie_chart, create_pie_chart2, create_bar_chart, \
    create_line_chart, get_recommendation, validate_recommender_data
from application.API.additional_functions import get_course_details, get_review_details
import pandas as pd
import datetime as dt
import json

scheduler = BackgroundScheduler()


# Create Charts on set intervals since it takes time
def create_charts():
    with app.app_context():

        # Fetching required data
        courses = Courses.query.all()
        year = dt.datetime.now().year
        data = {}
        for y in [year - 1, year]:
            for term in ["Jan", "May", "Sept"]:
                data[f"{term}_{y}"] = len(Enrollments.query.filter_by(term=term, year=y).all())
                # print(len(Enrollments.query.filter_by(term=term, year=year).all()))

        # print(data)
        # Creating Chart
        create_bar_chart(courses)
        create_pie_chart(courses)
        create_line_chart(data)
        create_pie_chart2(courses)
        print("Created charts...")


# Schedule the create_charts function to run every 4 hours
scheduler.add_job(create_charts, 'interval', seconds=60*60*4)
scheduler.start()


@app.route("/", methods=["GET"])
def hello():
    return  make_response(jsonify({"message": "Hello!, Welcome to Course Recommender API Server of Team 07 of Sept-2023, Please refer to API doc for help to use the server"}), 200)


# ------------------- Export Data API -----------------------
@app.route("/api/export_data", methods=["GET"])
def export():
    """API function to export all data of the application"""

    # Fetching all data from database
    users = Users.query.all()
    enrollments = Enrollments.query.all()
    courses = Courses.query.all()
    reviews = Reviews.query.all()

    # Converting all data object into dictionary
    users_data = [user.get_dictionary() for user in users]
    enrollments_data = [enroll.get_dictionary() for enroll in enrollments]
    courses_data = [course.get_dictionary() for course in courses]
    reviews_data = [review.get_dictionary() for review in reviews]

    # Making dataframe to save as excel later
    users_df = pd.DataFrame(users_data)
    enrollments_df = pd.DataFrame(enrollments_data)
    courses_df = pd.DataFrame(courses_data)
    reviews_df = pd.DataFrame(reviews_data)

    # Saving each dataframe in seperate sheet of excel workbook
    with pd.ExcelWriter('./application/Controller/static/output.xlsx', engine='xlsxwriter') as writer:
        users_df.to_excel(writer, sheet_name='Users', index=False)
        enrollments_df.to_excel(writer, sheet_name='Enrollments', index=False)
        courses_df.to_excel(writer, sheet_name='Courses', index=False)
        reviews_df.to_excel(writer, sheet_name="Reviews", index=False)

    return send_file('./application/Controller/static/output.xlsx', as_attachment=True, download_name='output.xlsx'), 200


# --------------------- Admin Courses List API------------------------
@app.route("/api/admin_courses_list", methods=["GET"])
def admin_courses_list():
    """API Function to get all courses list"""

    # Fetching all courses data and sending it as list of dictionaries
    courses = Courses.query.all()
    courses_list = []
    for course in courses:
        courses_list.append(get_course_details(course))

    return make_response(jsonify({"data": courses_list}), 200)


# ------------------Update Course Status API ------------------------
@app.route("/api/update_course_status", methods=["PUT"])
def update_course_status():
    """API Function to switch the active or inactive of course"""

    data = request.get_json()

    # Validating json dat
    if "course_id" not in data:
        return make_response(jsonify({"message": "course_id is required"}), 404)

    # Verifying if course_id is valid
    course_id = data["course_id"]
    course = Courses.query.get(course_id)
    if not course:
        return make_response(jsonify({"message": "Invalid Course Id"}), 404)

    try:
        # trying to save changes
        course.is_active = not course.is_active
        db.session.commit()
        return make_response(jsonify({"message": "Status Updated Successfully"}), 200)

    except:
        # Rolling back in case of failure
        db.session.rollback()
        return make_response(jsonify({"message": "Something went wrong..."}), 500)


# ------------------Admin Dashboard API --------------------------
@app.route("/api/admin_dashboard", methods=["GET"])
def admin_dashboard():
    """API Function for admin dashboard data"""
    date = dt.datetime.now()
    year = date.year
    month = date.month

    # identifying which term must be the current one based on current month
    if 1 <= month <= 4:
        term = "Jan"

    elif 5 <= month <= 8:
        term = "May"

    else:
        term = "Sept"

    # creating dictionary with required data fetched from database
    d = {
        "total_students": len(Users.query.all()),
        "total_courses": len(Courses.query.all()),
        "active_courses": len(Courses.query.filter_by(is_active=True).all()),
        "active_enrollments": len(Enrollments.query.filter_by(term=term, year=year).all())
    }

    return make_response(jsonify({"data": d}), 200)


# -------------------Get User's name -----------------
@app.route("/api/get_user_name/<int:user_id>", methods=["GET"])
def get_user_name(user_id):
    """API Function to get basic user detail"""

    # Verifying user_id is valid or not
    user = Users.query.get(user_id)
    if not user:
        return make_response(jsonify({"message": "Invalid User Id"}), 404)

    # Fetching all different values of level attribute in Courses
    levels = Courses.query.with_entities(Courses.level).distinct().all()
    l = []
    for level in levels:
        l.append(level[0])
    return make_response(jsonify({"data": {"user_id": user_id, "name": user.name, "levels": sorted(l)}}), 200)


# -----------------Course Recommender API---------------------
@app.route("/api/course_recommender", methods=["POST"])
def course_recommender():
    """API Function for getting course recommendation"""

    data = request.get_json()

    # Validating json data
    resp, status = validate_recommender_data(data)
    if not status:
        return resp

    user = Users.query.get(data["user_id"])
    if not user:
        return make_response(jsonify({"message": "user_id is invalid"}), 404)

    # Creating data dictionary for particular user
    user_data = {
        "side_work": user.side_work,
        "dual_degree": user.dual_degree,
        "num_courses": int(data["no_of_courses"]),
        "estimated_hours": int(data["study_hour"])
    }

    # fetching all courses of desired level
    courses = Courses.query.filter_by(level=data["level"]).all()

    if data["no_of_courses"] > len(courses):
        return make_response(jsonify({"data": f"Number of Courses available for level {data['level']} is less than "
                                              f"what you selected"}), 400)

    courses_data = {"course_id": [], "duration": [], "difficulty": [],
                    "rating": [], "support": []}

    # Creating required data list of dictionary of courses
    for course in courses:
        dt = get_review_details(course)
        courses_data["course_id"].append(course.course_id)
        courses_data["duration"].append(course.duration)
        courses_data["difficulty"].append(dt["avg_difficulty"])
        courses_data["rating"].append(dt["avg_rating"])
        courses_data["support"].append(dt["support"])

    # Fetching all enrollments for past data
    enrollments = Enrollments.query.all()
    enrollments_data = {"user_id": [], "course_id": [], "marks": [], "study_hour": []}

    # Creating required data list of dictionary of enrollments
    for enrollment in enrollments:
        enrollments_data["user_id"].append(enrollment.user_id)
        enrollments_data["course_id"].append(enrollment.course_id)
        enrollments_data["marks"].append(enrollment.marks)
        enrollments_data["study_hour"].append(enrollment.study_hours)


    try:
        # Trying to get the recommendation of courses
        recommended_courses = get_recommendation(user_data=user_data, courses_data=courses_data,
                                                 enrollments_data=enrollments_data, user_id=data["user_id"])

        recommended_data = []
        # finding course name of given recommended course ids
        for course_id, marks in zip(recommended_courses["course_id"], recommended_courses["estimated_marks"]):
            d = {}
            course = Courses.query.get(course_id)
            d["course_name"] = course.name
            d["estimated_marks"] = marks
            recommended_data.append(d)
        return make_response(jsonify({"data": recommended_data}), 200)

    except:

        # In case of failure , passing appropriate messages
        return make_response(jsonify({"data": "Something went wrong"}), 500)


# ------------------------Add Bulk Enrollments API----------------
@app.route("/api/add_bulk_enrollments", methods=["POST"])
def add_bulk_enrollments():
    """API Function for adding bulk enrollments using csv or excel file"""

    # Checking if file is passed
    if 'file' not in request.files:
        return make_response(jsonify({'message': 'No file part'}), 404)

    uploaded_file = request.files['file']

    # Checking if file is empty
    if uploaded_file.filename == '':
        return make_response(jsonify({'message': 'No selected file'}), 404)

    # Assuming the file is either CSV or Excel
    if uploaded_file.filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)

    # If not csv or excel file then sending format error
    else:
        return make_response(jsonify({"message": "Unsupported file format"}), 400)

    # Checking if all required columns are present in file
    required_columns = ["course_name", "username", "email", "marks", "term", "year", "study_hours"]

    # If all columns aren't present then finding missing column names and sending message
    if not all(column in df.columns for column in required_columns):
        missing_columns = [column for column in required_columns if column not in df.columns]
        return make_response(jsonify({"message": f"The Following Columns are missing: {missing_columns}"}), 404)

    # iterating over file data
    errors = []
    print(df.head(5))
    for index, row in df.iterrows():
        # Convert the row to a JSON object
        json_data = json.loads(row.to_json())

        # Checking if course exists for the course name
        c = Courses.query.filter_by(name=json_data["course_name"]).first()
        if c is not None:
            json_data["course_id"] = c.course_id

        else:
            # If not existing then skipping record and keeping a track of issue
            d = {"username": json_data["username"], "email": json_data["email"], "message": "Course name is invalid"}
            errors.append(d)
            continue

        # Checking if user exists for the username
        u = Users.query.filter_by(email=json_data["email"], username=json_data["username"]).first()
        if u is not None:
            json_data["user_id"] = u.user_id
        else:
            # If not existing then skipping record and keeping a track of the issue
            d = {"username": json_data["username"], "email": json_data["email"],
                 "message": "Either username/email or both are invalid or are not of same account"}

            errors.append(d)
            continue

        # Checking an enrollment exist for the user and course given in file
        enroll = Enrollments.query.filter_by(user_id=json_data["user_id"], course_id=json_data["course_id"]).first()

        # If exists then skipping record and keeping track of issue
        if enroll:
            d = {"username": json_data["username"], "email": json_data["email"],
                 "message": "Already Exists!"}
            errors.append(d)
            continue

        try:
            # Making Enrollment Object and trying to add and save database
            enroll = Enrollments(course_id=json_data["course_id"], user_id=json_data["user_id"], term=json_data["term"],
                                 year=json_data["year"], marks=json_data["marks"], study_hours=json_data["study_hours"])

            db.session.add(enroll)
            db.session.commit()

        except:
            # In case of failure, storing the issue
            d = {"username": json_data["username"], "email": json_data["email"],
                 "message": "Something went wrong!!"}
            errors.append(d)

    # If there are any errors then sending errors list
    if len(errors) > 0:
        return make_response(jsonify({"data": errors}), 400)

    # If everything is perfect then sending success message
    return make_response(jsonify({"message": "Successfully added all"}), 200)



