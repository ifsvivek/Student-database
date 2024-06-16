from flask import Flask, request, render_template
from functions import create_connection, insert_student_marks
from flask import jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
host_name = os.getenv("HOST_NAME")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
db_name = os.getenv("DB_NAME")

connection = create_connection(host_name, user_name, password, db_name)


@app.route("/")
def form():
    return render_template("index.html")


@app.route("/insert_student_marks", methods=["POST"])
def insert_marks():
    usn = request.form.get("usn")
    name = request.form.get("name")
    age = request.form.get("age")
    branch = request.form.get("branch")
    total_marks = request.form.get("total_marks")
    insert_student_marks(connection, usn, name, age, branch, total_marks)
    return {"message": "Student marks inserted successfully."}


@app.route("/get_all_students", methods=["GET"])
def get_all_students():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = [
        dict((cursor.description[i][0], value) for i, value in enumerate(row))
        for row in cursor.fetchall()
    ]
    return jsonify(students)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
