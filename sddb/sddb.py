from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="1234", database="appy"
    )

# Create the employee table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS employee (
                        ssn VARCHAR(20) PRIMARY KEY,
                        fname VARCHAR(50),
                        lname VARCHAR(50),
                        bdate VARCHAR(20),
                        address VARCHAR(200),
                        sex VARCHAR(10),
                        salary FLOAT,
                        super_ssn VARCHAR(20),
                        deptno INT)"""
    )
    conn.commit()
    cursor.close()
    conn.close()

create_table()

@app.route("/")
def index():
    return render_template("index.html")

# Route to insert an employee
@app.route("/employee", methods=["POST"])
def create_employee():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO employee (ssn, fname, lname, bdate, address, sex, salary, super_ssn, deptno)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            data["ssn"],
            data["fname"],
            data["lname"],
            data["bdate"],
            data["address"],
            data["sex"],
            data["salary"],
            data["super_ssn"],
            data["deptno"],
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Employee created successfully"}), 201

# Route to get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees), 200

# Route to get a specific employee by ssn
@app.route("/employee/<ssn>", methods=["GET"])
def get_employee(ssn):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee WHERE ssn = %s", (ssn,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    return jsonify(employee), 200

# Route to update an employee by ssn
@app.route("/employee/<ssn>", methods=["PUT"])
def update_employee(ssn):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE employee SET fname = %s, lname = %s, bdate = %s, address = %s,
                      sex = %s, salary = %s, super_ssn = %s, deptno = %s WHERE ssn = %s""",
        (
            data["fname"],
            data["lname"],
            data["bdate"],
            data["address"],
            data["sex"],
            data["salary"],
            data["super_ssn"],
            data["deptno"],
            ssn,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Employee updated successfully"}), 200

# Route to delete an employee by ssn
@app.route("/employee/<ssn>", methods=["DELETE"])
def delete_employee(ssn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE ssn = %s", (ssn,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Employee deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)