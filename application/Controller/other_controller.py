from user_controller import app
from flask import request, render_template, flash, redirect
from constants import ADMINS
import requests
import json
import pandas as pd


# For getting full list of courses for admin
@app.route("/<int:user_id>/admin_courses_list", methods=["GET", "POST"])
def admin_courses_list(user_id):
    """Controller Function for handling admin courses lists"""

    # Ensuring it's the admin only
    if user_id not in ADMINS:
        return "Forbidden!! Admins only!", 403

    # For get request hitting api and rendering template with data
    if request.method == "GET":
        response = requests.get("http://127.0.0.1:5001/api/admin_courses_list")
        if response.status_code == 200:
            course_data = response.json()["data"]
            data = {"user_id": user_id}
            return render_template("admin_courses_list.html", page_title="Courses List", courses=course_data,
                                   user_id=user_id, data=data, admin=True)

        return response.json()

    # In case of post request, updating the status of particular course via API
    elif request.method == "POST":
        course_id = request.form["course_id"]
        data = json.dumps({"course_id": course_id})
        headers = {"Content-Type": "application/json"}
        response = requests.put("http://127.0.0.1:5001/api/update_course_status", data=data,
                                headers=headers)

        # If api response is success then reverting to admin course page
        if response.status_code == 200:
            return redirect(f"/{user_id}/admin_courses_list")

        # Else returning appropriate message
        data = response.json()
        return data["message"]


# For Admin Dashboard
@app.route("/<int:user_id>/admin_dashboard", methods=["GET"])
def admin_dashboard(user_id):
    """Controller Function for handling admin dashboard"""

    # Hitting API to get data
    response = requests.get("http://127.0.0.1:5001/api/admin_dashboard")

    # rendering template if API response is a success
    if response.status_code == 200:
        data = response.json()["data"]
        data["user_id"] = user_id
        return render_template("dashboard.html", page_title="Admin Dashboard", data=data, user_id=user_id,
                               admin=True)

    # in case of failure response, passing appropriate message
    return response.json()


# For Course Recommender
@app.route("/<int:user_id>/course_recommender", methods=["GET", "POST"])
def course_recommender(user_id):
    """Controller Function for handling course recommender functionality"""

    # hitting API to get basic info about user
    response = requests.get(f"http://127.0.0.1:5001/api/get_user_name/{user_id}")

    if response.status_code == 200:
        data = response.json()["data"]
        info = {"user_id": user_id}

        # In case of POST request, fetching data
        if request.method == "POST":
            no_of_courses = int(request.form["no_of_courses"])
            study_hour = int(request.form["study_hour"])
            level = int(request.form["level"])

            # Making json and hitting API
            data1 = json.dumps({"user_id": user_id, "no_of_courses": no_of_courses, "study_hour": study_hour,
                               "level": level})
            headers = {"Content-Type": "application/json"}
            response1 = requests.post("http://127.0.0.1:5001/api/course_recommender", data=data1, headers=headers)

            # Upon success, taking out data and showing the recommendation on page
            if response1.status_code == 200:
                data1 = response1.json()["data"]

                return render_template("course_recommender.html", suggest=True, courses=data1, levels=data["levels"],
                                       user_id=data["user_id"], data=info)

            elif response1.status_code == 400:
                msg = response1.json()["data"]
                flash(msg)
                return redirect(f"/{user_id}/course_recommender")

            # In case of failure, showing appropriate message
            elif response1.status_code == 500:

                msg = response1.json()["data"]
                flash(msg)
                return redirect(f"/{user_id}/course_recommender")

            return response1.json()

        return render_template("course_recommender.html", page_title="Course Recommender", name=data["name"],
                               levels=data["levels"], user_id=user_id, data=info)

    return response.json()


# Controller for adding bulk enrollments
@app.route("/<int:user_id>/add_enrollments/admin", methods=["POST"])
def add_bulk_enrollments(user_id):
    """Controller Function for adding bulk enrollments"""

    if request.method == "POST":
        # Taking out file
        enroll_file = request.files["add_enrollment"]

        # Preparing data to send to API
        files = {'file': (enroll_file.filename, enroll_file.stream, enroll_file.mimetype)}
        response = requests.post("http://127.0.0.1:5001/api/add_bulk_enrollments", files=files)
        data_1 = response.json()
        data = {"user_id": user_id}

        # If response is success then rendering page with success message
        if response.status_code == 200:
            return render_template("enrollments_report.html", page_title="Enrollment Reports", admin=True,
                                   records=data_1["data"], data=data, success=True)

        # If response is failure then rendering page with errors list
        return render_template("enrollments_report.html", page_title="Enrollment Reports", admin=True,
                               records=data_1["data"], data=data, success=False)

