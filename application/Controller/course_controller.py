from user_controller import app
from flask import request, render_template, flash, redirect
from constants import ADMINS
import requests
import json


# For student dashboard
@app.route("/courses/student/<user_id>", methods=["GET"])
def student_dashboard(user_id):
    """Controller Function for handling Student dashboard"""

    # Hitting APIs to get the data of that student
    resp = requests.get(f"http://127.0.0.1:5001/api/courses/student/{user_id}")

    # If success then rendering template with data
    if resp.status_code == 200:
        json_data = resp.json()
        return render_template("course_list.html", data=json_data, page_title="Student Dashboard", user_id=user_id)

    # In case of failure, sending appropriate message
    elif resp.status_code == 404:
        return resp.json()["message"]

    return resp.json()


# For viewing course details
@app.route("/<int:user_id>/course/<int:course_id>", methods=["GET"])
def view_course(user_id, course_id):
    """Controller Function for handling view course page"""

    # Hitting API to get course details
    resp = requests.get(f"http://127.0.0.1:5001/api/course/{course_id}")

    # If success then rendering template
    if resp.status_code == 200:
        json_data = resp.json()
        json_data["user_id"] = user_id
        # Checking if it's an admin or normal student
        if user_id not in ADMINS:
            return render_template("course_page.html", page_title="Course Page", data=json_data["data"],
                                   user_id=user_id, admin=False)

        return render_template("course_page.html", page_title="Course Page", data=json_data["data"],
                               user_id=user_id, admin=True)

    # In case of failure, sending appropriate message
    elif resp.status_code == 404:
        return resp.json()
    return "API server is not started, Please start API server", 500


# For Adding course
@app.route("/<int:user_id>/add_course", methods=["GET", "POST"])
def add_course(user_id):
    """Controller Function for handling add course functionality"""
    if user_id not in ADMINS:
        return "Forbidden! Admins Only!", 403

    data = {"user_id": user_id}

    # In case of get request rendering,
    if request.method == "GET":
        return render_template("add_course.html", page_title="Add Course", user_id=user_id, admin=True, data=data)

    # In case of post request getting data
    else:
        var_name = request.form['name']
        var_code = request.form['code']
        var_type = request.form['type']
        var_duration = request.form['duration']
        var_professor = request.form['professor']
        var_level = request.form['level']
        var_description = request.form['description']

        # preparing data for hitting API
        data = json.dumps({
            "name": var_name,
            "code": var_code,
            "duration": var_duration,
            "professor": var_professor,
            "course_type": var_type,
            "level": var_level,
            "description": var_description,
        })

        headers = {"Content-Type": "application/json"}
        response = requests.post("http://127.0.0.1:5001/api/course", data=data, headers=headers)

        # getting response message
        msg = response.json()["message"]
        flash(msg)
        if response.status_code == 201:
            return redirect(f"/{user_id}/admin_courses_list")

        return render_template("add_course.html", page_title="Add Course", user_id=user_id, admin=True, data=data)


# For editing Course
@app.route("/<int:user_id>/edit_course/<course_id>", methods=["GET", "POST"])
def edit_course(user_id, course_id):
    """Controller Function for handling edit course functionality"""

    # Ensuring the user is admin
    if user_id not in ADMINS:
        return "Forbidden!! Only Admins are Allowed", 403

    # In case of get request, Hitting api to get course data

    resp = requests.get(f"http://127.0.0.1:5001/api/course/{course_id}")
    if resp.status_code == 200:
        json_data = resp.json()

    # In case of post request getting modified data
    if request.method == "POST":
        var_name = request.form['name']
        var_code = request.form['code']
        var_type = request.form['type']
        var_duration = request.form['duration']
        var_professor = request.form['professor']
        var_level = request.form['level']
        var_description = request.form['description']

        # preparing data as json and hitting API to modify
        data = json.dumps({
            "name": var_name,
            "code": var_code,
            "duration": var_duration,
            "professor": var_professor,
            "course_type": var_type,
            "level": var_level,
            "description": var_description,
        })

        headers = {"Content-Type": "application/json"}
        response = requests.put(f"http://127.0.0.1:5001/api/course/{course_id}", data=data, headers=headers)
        msg = response.json()["message"]
        flash(msg)

        # If modified successfully then reverting to view course page
        if response.status_code == 200:
            return redirect(f"/{user_id}/course/{course_id}")
        # In case of failure reverting to current page with appropriate message
        else:
            return render_template("edit_course.html", page_title="Edit Course", data=json_data["data"], admin=True,
                                   user_id=user_id)

    # Rendering template for get request
    return render_template("edit_course.html", page_title="Edit Course", data=json_data["data"], admin=True,
                           user_id=user_id)


# For deleting course
@app.route("/<int:user_id>/delete_course/<int:course_id>", methods=["GET"])
def delete_course(user_id, course_id):
    response = requests.delete(f"http://127.0.0.1:5001/api/course/{course_id}")
    msg = response.json()["message"]
    flash(msg)
    return redirect(f"/{user_id}/admin_courses_list")

