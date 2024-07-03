from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from prettytable import PrettyTable

app = Flask(__name__)


def create_connection():
    cnx = mysql.connector.connect(
        user="root",
        password="1234",
        host="localhost",
        database="library",
    )
    return cnx


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/enter_data", methods=["GET", "POST"])
def enter_data():
    if request.method == "POST":
        table = request.form["table"]
        data = ()
        if table == "BOOKS":
            data = (
                request.form["field1"],
                request.form["field2"],
                request.form["field3"],
                request.form["field4"],
                request.form["field5"],
            )
            query = "INSERT INTO BOOKS (BOOK_ID, AUTHOR_NAME, TITLE, EDITION, PRICE) VALUES (%s, %s, %s, %s, %s)"
        elif table == "PUBLISHER":
            data = (
                request.form["field1"],
                request.form["field2"],
                request.form["field3"],
            )
            query = "INSERT INTO PUBLISHER (P_ID, PNAME, YOP) VALUES (%s, %s, %s)"
        elif table == "PUBLISHES":
            data = (
                request.form["field1"],
                request.form["field2"],
            )
            query = "INSERT INTO PUBLISHES (BOOK_ID, P_ID) VALUES (%s, %s)"

        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        return redirect(url_for("index"))
    return render_template("enter_data.html", table=request.args.get("table"))


@app.route("/display_data/<table>")
def display_data(table):
    cnx = create_connection()
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template("display_data.html", data=data, table=table)


if __name__ == "__main__":
    app.run(debug=True)
