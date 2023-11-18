from flask import make_response, jsonify
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from numpy import linspace
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


matplotlib.use('TkAgg')


def validate_enroll_data(data):
    """Function to get validate enroll data"""

    if "course_id" not in data:
        return make_response(jsonify({"message": "course_id is required"}), 404), False

    if not isinstance(data["course_id"], int):
        return make_response(jsonify({"message": "course_id should be integer"}), 400), False

    if "user_id" not in data:
        return make_response(jsonify({"message": "user_id is required"}), 404), False

    if not isinstance(data["user_id"], int):
        return make_response(jsonify({"message": "user_id should be integer"}), 400), False

    resp, status = validate_update_enroll_data(data)

    if not status:
        return resp, False

    return None, True


def validate_update_enroll_data(data):
    """Function to validate update enroll data"""

    if "marks" not in data:
        return make_response(jsonify({"message": "marks is required"}), 404), False

    if not isinstance(data["marks"], int):
        return make_response(jsonify({"message": "marks should be integer"}), 400), False

    if "year" not in data:
        return make_response(jsonify({"message": "year is required"}), 404), False

    if not isinstance(data["year"], int):
        return make_response(jsonify({"message": "year should be integer"}), 400), False

    if "study_hours" not in data:
        return make_response(jsonify({"message": "study_hours is required"}), 404), False

    if not isinstance(data["study_hours"], int):
        return make_response(jsonify({"message": "study_hours should be integer"}), 400), False

    if "term" not in data:
        return make_response(jsonify({"message": "term is required"}), 404), False

    if len(data["term"].strip()) == 0:
        return make_response(jsonify({"message": "term cannot be empty"}), 400), False

    if not data["term"].isalpha():
        return make_response(jsonify({"message": "term can only be alphabets"}), 400), False

    return None, True


def create_pie_chart(courses):
    """Function to create pie chart for given courses"""

    labels = []
    sizes = []
    for course in courses:
        labels.append(course.name)
        sizes.append(len(course.enrollments))

    # Create a pie chart
    plt.figure(figsize=(3, 3), dpi=200)  # Optional: Set the figure size
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 5})

    # Set the title for the chart
    plt.title('Student Distribution by Courses', fontsize=7)
    plt.tight_layout()
    plt.savefig("./application/Controller/static/images/chart1.jpg")


def create_bar_chart(courses):
    """Function to create bar chart for the courses"""
    count = {}
    for course in courses:
        if course.course_type in count:
            count[course.course_type] += 1
        else:
            count[course.course_type] = 1

    cmap = get_cmap('viridis')
    plt.figure(figsize=(2, 4), dpi=200)  # Optional: Set the figure size
    plt.bar(count.keys(), count.values(), color=cmap(linspace(0, 1, len(count.keys()))))

    # Set the title for the chart
    plt.title('Courses Distribution by categories', fontsize=6)
    plt.yticks(fontsize=5)
    plt.xticks(fontsize=5, rotation=45)

    plt.tight_layout()
    plt.savefig("./application/Controller/static/images/chart2.jpg")


def create_line_chart(data):
    """Function to get create line chart for the data"""

    plt.figure(figsize=(3, 3), dpi=200)  # Optional: Set the figure size
    plt.plot(data.keys(), data.values(), "g--", linewidth=2)

    # Set the title for the chart
    plt.title('Enrollments by Terms', fontsize=6)
    plt.ylim(0, max(data.values()) + 5)
    plt.yticks(fontsize=5)
    plt.xticks(fontsize=5, rotation=45)

    plt.tight_layout()
    plt.savefig("./application/Controller/static/images/chart3.jpg")


def create_pie_chart2(courses):
    """Function to get create different pie chart for the courses"""

    labels = []
    sizes = []
    for course in courses:
        labels.append(course.name)
        sizes.append(len(course.reviews))

    cmap = get_cmap('viridis')
    # Create a pie chart
    plt.figure(figsize=(3, 3), dpi=200)  # Optional: Set the figure size
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 5},
            colors=cmap(linspace(0.5, 1, len(labels))))

    # Set the title for the chart
    plt.title('Reviews Distribution by Courses', fontsize=7)
    plt.tight_layout()
    plt.savefig("./application/Controller/static/images/chart4.jpg")


def get_recommendation(user_data, courses_data, enrollments_data, user_id):
    """Function to get recommended courses"""

    # Preprocess user and course data
    courses_data = pd.DataFrame(courses_data)
    enrollments_data = pd.DataFrame(enrollments_data)

    user_courses = pd.DataFrame([user_data] * len(courses_data))
    user_courses = pd.concat([user_courses, courses_data], axis=1)
    # Merge with enrollment data
    user_courses = pd.merge(user_courses, enrollments_data, how='left', on='course_id')

    # Calculate TF-IDF for textual features
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(user_courses.astype(str).values.ravel())

    # Calculate cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    recommended_courses = recommend_courses(user_courses=user_courses, course_data=courses_data, cosine_sim=cosine_sim,
                                            num_courses=user_data["num_courses"], user_id=user_id)

    return recommended_courses


def recommend_courses(user_courses, course_data, cosine_sim, num_courses, user_id):
    """Function to get recommended courses and marks"""

    user_index = len(course_data)  # Assuming the user is added as the last row
    sim_scores = list(enumerate(cosine_sim[user_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:num_courses + 1]  # Exclude the user itself from recommendations
    course_indices = [i[0] - 1 for i in sim_scores]
    recommended_courses = course_data.iloc[course_indices].reset_index(drop=True)

    # Estimate marks for recommended courses
    estimated_marks = []
    for course_id in recommended_courses['course_id']:
        # Filter past enrollments for the recommended course
        past_enrollments = user_courses[(user_courses['course_id'] == course_id)]

        if not past_enrollments.empty:
            # Calculate weighted average of marks based on study hours
            weighted_average = (past_enrollments['marks'] * past_enrollments['study_hour']).sum() / past_enrollments[
                'study_hour'].sum()
            estimated_marks.append(weighted_average)
        else:
            # If no past enrollment, provide a default estimated mark
            estimated_marks.append(50)

    recommended_courses['estimated_marks'] = estimated_marks
    return recommended_courses


def validate_recommender_data(data):
    """Function to validate recommender data"""

    if "user_id" not in data:
        return make_response(jsonify({"message": "user_id is required"}), 404), False

    if not isinstance(data["user_id"], int):
        return make_response(jsonify({"message": "user_id should be integer"}), 400), False

    if "no_of_courses" not in data:
        return make_response(jsonify({"message": "no_of_courses is required"}), 404), False

    if not isinstance(data["no_of_courses"], int):
        return make_response(jsonify({"message": "no_of_courses should be integer"}), 400), False

    if "study_hour" not in data:
        return make_response(jsonify({"message": "study_hour is required"}), 404), False

    if not isinstance(data["study_hour"], int):
        return make_response(jsonify({"message": "study_hour should be integer"}), 400), False

    if "level" not in data:
        return make_response(jsonify({"message": "level is required"}), 404), False

    if not isinstance(data["level"], int):
        return make_response(jsonify({"message": "level should be integer"}), 400), False

    return None, True

