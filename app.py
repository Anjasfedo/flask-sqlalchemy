from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

file_path = os.path.abspath(os.getcwd()) + "\\test.db"

print("Database file path:", file_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

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
    with app.app_context():
        db.create_all()
        app.run(debug=True)
