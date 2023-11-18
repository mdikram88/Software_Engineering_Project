from flask import Flask
from application.API.models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Importing database instance and integrating with Flask app
db.init_app(app)
app.app_context().push()

# db.create_all()


from application.API.user_api import *



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
