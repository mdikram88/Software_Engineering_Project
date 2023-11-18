from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


## Users
class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    reset_code = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False, unique=True)
    dual_degree = db.Column(db.Boolean, nullable=False)
    side_work = db.Column(db.Boolean, nullable=False)
    additional_education = db.Column(db.String(100))
    verified = db.Column(db.Boolean, nullable=False)
    enrollments = relationship("Enrollments", back_populates="enroll_student")
    reviews = relationship("Reviews", back_populates="student")

    def __init__(self, name, username, email, password, reset_code, roll_no,
                 dual_degree, side_work, additional_education, verified=False):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.reset_code = reset_code
        self.roll_no = roll_no
        self.dual_degree = dual_degree
        self.side_work = side_work
        self.additional_education = additional_education
        self.verified = verified

    def get_dictionary(self):
        dt = {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "reset_code": self.reset_code,
            "dual_degree": self.dual_degree,
            "side_work": self.side_work,
            "verified": self.verified
        }
        return dt


## Enrollments


class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    term = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    study_hours = db.Column(db.Integer, nullable=False)
    enroll_student = relationship("Users", back_populates="enrollments")
    enroll_course = relationship("Courses", back_populates="enrollments")

    def __init__(self, course_id, user_id, marks, term, year, study_hours):
        self.course_id = course_id
        self.user_id = user_id
        self.marks = marks
        self.term = term
        self.year = year
        self.study_hours = study_hours

    def get_dictionary(self):
        dt = {
            "enrollment_id": self.enrollment_id,
            "course_id": self.course_id,
            "user_id": self.user_id,
            "marks": self.marks,
            "term": self.term,
            "year": self.year,
            "study_hour": self.study_hours
        }
        return dt


# Course

class Courses(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    professor = db.Column(db.String(50), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    level = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    enrollments = relationship("Enrollments", back_populates="enroll_course")
    reviews = relationship("Reviews", back_populates="course")

    def __init__(self, code, name, description, professor, course_type, duration, level, is_active=False):
        self.code = code
        self.name = name
        self.description = description
        self.professor = professor
        self.course_type = course_type
        self.duration = duration
        self.level = level
        self.is_active = is_active

    def get_dictionary(self):
        dt = {
            "course_id": self.course_id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "professor": self.professor,
            "course_type": self.course_type,
            "duration": self.duration,
            "level": self.level,
            "is_active": self.is_active
        }
        return dt


# Reviews

class Reviews(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review = db.Column(db.Text)
    difficulty = db.Column(db.Integer, nullable=False)
    support = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    student = relationship("Users", back_populates="reviews")
    course = relationship("Courses", back_populates="reviews")

    def __init__(self, review, difficulty, support, rating, user_id, course_id):
        self.review = review
        self.difficulty = difficulty
        self.support = support
        self.rating = rating
        self.user_id = user_id
        self.course_id = course_id

    def get_dictionary(self):
        dt = {
            "review_id": self.review_id,
            "review": self.review,
            "difficulty": self.difficulty,
            "support": self.support,
            "rating": self.rating,
            "user_id": self.user_id,
            "course_id": self.course_id
        }

        return dt
