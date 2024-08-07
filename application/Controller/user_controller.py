from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import requests, json
from constants import ADMINS

app = Flask(__name__)

app.secret_key = "this_is_secret_key"


# Controller for Login
@app.route("/", methods=['GET', 'POST'])
def login():
    """Controller function handling login functionality"""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        data = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}

        # hitting API to verify the details
        response = requests.post("http://127.0.0.1:5001/api/login", data=data, headers=headers)

        # if everything is fine then forwarding to dashboard
        if response.status_code == 200:

            data = response.json()

            # Checking if user is an admin or student
            if data["user_id"] in ADMINS:
                return redirect(f"/{data['user_id']}/admin_dashboard")
            return redirect(f"/courses/student/{data['user_id']}")
        else:
            # In case of failure of verification giving appropriate message
            data = response.json()
            flash(data["message"])
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Login Page")


# Controller for Sign up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Controller Function for handling Sign Up functionality"""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        username = request.form["username"]
        roll_no = request.form["roll_no"]
        reset = request.form["reset_code"]
        dual_degree = json.loads((request.form["dual_degree"]).lower())
        side_work = json.loads((request.form["side_work"]).lower())
        additional_education = request.form["additional_education"]

        # putting data as json and hitting API for creating new account
        data = json.dumps({"email": email, "additional_education": additional_education,"side_work": side_work,
                           "dual_degree":dual_degree,"password": password, "roll_no":roll_no ,"name": name,
                           "username": username, "reset_code": reset})

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url="http://127.0.0.1:5001/api/signup", data=data, headers=headers)
        flash(response.json()["message"])

        # If account created successfully reverting to login page
        if response.status_code == 201:
            return redirect("/")

        else:
            # In case of error rendering same page with message
            return render_template("signup.html")

    return render_template("signup.html")


# Controller for Forget Password
@app.route("/forgetpassword", methods=["GET", "POST"])
def forget_password():
    """Controller Function for handling forget password functionality"""

    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]
        reset_code = request.form["reset_code"]

        # Preparing data into json to hit API for password reset
        data = json.dumps({"username": username, "new_password": new_password, "reset_code": reset_code})
        headers = {"Content-Type": "application/json"}

        response = requests.post(url="http://127.0.0.1:5001/api/forget_password", data=data, headers=headers)

        flash(response.json()["message"])

        # If password is reset successfully then reverting to login page with message
        if response.status_code == 202:
            return redirect("/")

        else:
            # In case of failure due to some reason then rendering back the page with message
            return render_template("forgetpassword.html")

    return render_template("forgetpassword.html")


# Controller for view profile
@app.route("/view_profile/<user_id>", methods=["GET"])
def view_profile(user_id):
    """Controller Function for handling view profile functionality"""

    # hitting API for getting user details
    resp = requests.get(f"http://127.0.0.1:5001/api/profile/{user_id}")

    # If response will be success
    if resp.status_code == 200:
        json_data = resp.json()
        if json_data["data"]["user_id"] in ADMINS:
            return render_template("view_profile.html", data=json_data["data"], page_title="View Profile", admin=True)
        return render_template("view_profile.html", data=json_data["data"], page_title="View Profile", admin=False)

    # In case of failure
    data = resp.json()
    return data, 500


# Controller for edit profile
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    """Controller Function for handling edit profile functionality"""

    # Hitting API to get details of the user
    resp = requests.get(f"http://127.0.0.1:5001/api/profile/{user_id}")

    # In case of success and request type is 'GET' then rendering the template with the data
    if resp.status_code == 200:
        json_data = resp.json()
        data = json_data["data"]

        # If it's post request then taking modified data
        if request.method == "POST":
            var_name = request.form['name']
            var_email = request.form['email']
            var_password = request.form['password']
            var_reset_code = request.form['reset_code']
            var_dual_degree = json.loads((request.form['dual_degree']).lower())
            var_side_work = json.loads((request.form['side_work']).lower())
            var_additional_education = request.form['additional_education']

            # Preparing it as json data and hitting API for modifying
            data = json.dumps({
                "name": var_name,
                "email": var_email,
                "password": var_password,
                "username": data["username"],
                "reset_code": var_reset_code,
                "dual_degree": var_dual_degree,
                "side_work": var_side_work,
                "additional_education": var_additional_education,
            })

            headers = {"Content-Type": "application/json"}
            response = requests.put(f"http://127.0.0.1:5001/api/profile/{user_id}", data=data, headers=headers)

            # Taking response and flashing message
            msg = response.json()["message"]
            flash(msg)

            # In case of success it will revert to view profile page
            if response.status_code == 202:
                return redirect(f"/view_profile/{user_id}")

            # In case of failure it will go back to edit profile with appropriate message
            return redirect(f"/edit_profile/{user_id}")

        return render_template("edit_profile.html", page_title="Edit Profile", data=json_data["data"])
    data = resp.json()
    return data, resp.status_code


# Controller for New Students
@app.route("/<int:user_id>/new_students/admin")
def new_students(user_id):
    """Controller Function for handling new students list Page"""

    # hitting API to get data
    req = requests.get("http://127.0.0.1:5001/api/new_students")

    # If response is success then rendering template with data
    if req.status_code == 200:
        info = req.json()["data"]
        data = {"user_id": user_id}
        return render_template("new_students.html", data=data, students=info, admin=True, page_title="New Students List")

    # If response is failure then returning status code
    return req.status_code


# Controller for approving students
@app.route("/<int:user_id>/student/approve", methods=["GET"])
def approve_student(user_id):
    """Controller Function for handling approve functionality"""

    data = json.dumps({"user_id": user_id})
    headers = {"Content-Type": "application/json"}

    # hitting API to update student status
    req = requests.put("http://127.0.0.1:5001/api/student/approve", data=data, headers=headers)
    msg = req.json()["message"]
    flash(msg)
    return redirect(f"/{user_id}/new_students/admin")


from course_controller import *
from other_controller import *
from review_controller import *
from enrollment_controller import *


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")