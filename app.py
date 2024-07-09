from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from models import db, User

file_path = os.path.abspath(os.getcwd()) + "\\test.db"

print("Database file path:", file_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        # Create a new User object
        new_user = User(username=username, email=email)

        # Add the new User object to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()

        print(f"User '{username}' with email '{email}' added to the database.")

    users = User.query.all()

    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
