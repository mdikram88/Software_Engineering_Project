from user_controller import app
from flask import request, render_template, flash, redirect
from constants import ADMINS
import requests
import json


@app.route("/<int:user_id>/add_review_by_course", methods=["GET", "POST"])
def add_review_by_course(user_id):

    if user_id in ADMINS:
        return "Forbidden!! Students Only", 403

    data1 = json.dumps({"user_id": user_id, "enrollment_type": "enrolled"})
    headers = {"Content-Type": "application/json"}

    req2 = requests.post("http://127.0.0.1:5001/api/courses/student", data=data1, headers=headers)
    courses = []
    if req2.status_code == 200:
        courses = req2.json()["data"]

    # In case of post request, taking out form data and hitting API for adding review
    if request.method == "POST":
        course_id = int(request.form["course_name"])
        difficulty = int(request.form["difficulty"])
        support = int(request.form["support"])
        rating = int(request.form["rating"])
        review = request.form["review"]
        data = json.dumps({"user_id": user_id, "course_id": course_id ,"difficulty": difficulty, "support": support, "rating": rating,
                           "review": review})

        headers = {"Content-Type": "application/json"}
        resp = requests.post("http://127.0.0.1:5001/api/review", data=data, headers=headers)

        # In case of success, sending back to review list
        if resp.status_code == 201:
            msg = resp.json()["message"]
            flash(msg)
            return redirect(f"/{user_id}/reviews/student")

        # In case of failure sending back to add review page with appropriate message
        msg = resp.json()["message"]
        flash(msg)
        return redirect(f"/{user_id}/add_review_by_course")

    data = {"user_id": user_id}

    return render_template("add_review_by_course.html", data=data, user_id=user_id, courses=courses)



@app.route("/<int:user_id>/add_review/<int:course_id>", methods=["GET", "POST"])
def add_review(user_id, course_id):
    """Controller Function for handling add review for particular course"""
    if user_id in ADMINS:
        return "Forbidden!! Students Only", 403

    # In case of post request, taking out form data and hitting API for adding review
    if request.method == "POST":
        difficulty = int(request.form["difficulty"])
        support = int(request.form["support"])
        rating = int(request.form["rating"])
        review = request.form["review"]
        data = json.dumps({"user_id": user_id, "course_id": course_id ,"difficulty": difficulty, "support": support, "rating": rating,
                           "review": review})

        headers = {"Content-Type": "application/json"}
        resp = requests.post("http://127.0.0.1:5001/api/review", data=data, headers=headers)

        # In case of success, sending back to review list
        if resp.status_code == 201:
            msg = resp.json()["message"]
            flash(msg)
            return redirect(f"/{user_id}/reviews/student")

        # In case of failure sending back to add review page with appropriate message
        msg = resp.json()["message"]
        flash(msg)
        return redirect(f"/{user_id}/add_review/{course_id}")

    data = {"user_id": user_id, "course_id": course_id}
    resp = requests.get(f"http://127.0.0.1:5001/api/course/{course_id}")

    if resp.status_code == 200:
        info = resp.json()["data"]
        data["course_name"] = info["name"]

    return render_template("add_review.html", data=data, user_id=user_id)


@app.route("/<int:user_id>/view_review/<int:review_id>", methods=["GET"])
def view_review(review_id, user_id):
    """Controller Function for handling view review functionality"""

    # Hitting API to get review data
    resp = requests.get(f"http://127.0.0.1:5001/api/review/{review_id}")

    # In case of success, rendering page with data
    if resp.status_code == 200:
        data = resp.json()["data"]
        return render_template("view_review.html", data=data, user_id=user_id)

    return resp.json()["message"]


@app.route("/<int:user_id>/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(user_id, review_id):
    """Controller Function for handling edit review functionality"""

    # Hitting API to get review data
    response = requests.get(f"http://127.0.0.1:5001/api/review/{review_id}")

    # If response is success, rendering Edit Review form
    if response.status_code == 200:
        info = response.json()["data"]

        # In case of POST request, fetching out data from form
        if request.method == "POST":
            difficulty = int(request.form["difficulty"])
            support = int(request.form["support"])
            rating = int(request.form["rating"])
            review = request.form["review"]

            # Making json and passing on API for editing review
            data = json.dumps({"review_id": review_id, "difficulty": difficulty, "support": support, "rating": rating,
                               "review": review})

            headers = {"Content-Type": "application/json"}
            resp = requests.put("http://127.0.0.1:5001/api/review", data=data, headers=headers)
            data = resp.json()["message"]
            flash(data)
            # Upon success, reverting to view page
            if resp.status_code == 202:
                return redirect(f"/{user_id}/view_review/{review_id}")

            # Upon failure, sending appropriate message
            return render_template("edit_review.html", data=info, user_id=user_id)

        # Rendering template for GET request of edit review
        return render_template("edit_review.html", data=info, user_id=user_id)

    return response.json()


@app.route("/<int:user_id>/delete_review/<int:review_id>", methods=["GET"])
def delete_review(user_id, review_id):
    """Controller Function for handling delete review functionality"""

    data = json.dumps({"review_id": review_id})
    headers = {"Content-Type": "application/json"}

    # Hitting API for deleting Review
    response = requests.delete(f"http://127.0.0.1:5001/api/review/{review_id}", data=data, headers=headers)

    # Taking out message
    msg = response.json()["message"]
    flash(msg)

    # If success, redirecting to student's review page
    if response.status_code == 200:
        return redirect(f"/{user_id}/reviews/student")

    # in case of failure redirecting to student's review page with message
    return redirect(f"/{user_id}/reviews/student")


@app.route("/<int:user_id>/reviews/student", methods=["GET"])
def student_reviews(user_id):
    """Controller Function for handling Student Reviews List Functionality"""

    # Hitting API to get Student's reviews
    response = requests.get(f"http://127.0.0.1:5001/api/reviews/student/{user_id}")

    # In case of success, rendering template with data
    if response.status_code == 200:
        review_data = response.json()["data"]
        data = {"user_id": user_id}
        return render_template("student_reviews.html", reviews=review_data, user_id=user_id, data=data)

    return response.json()
