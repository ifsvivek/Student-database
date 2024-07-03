from flask import *
import mysql.connector

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


@app.route("/delete_data/<table>/<id>", methods=["POST"])
def delete_data(table, id):
    cnx = create_connection()
    cursor = cnx.cursor()
    query = f"DELETE FROM {table} WHERE ID = %s"
    cursor.execute(query, (id,))
    cnx.commit()
    cursor.close()
    return redirect(url_for("display_data", table=table))


@app.route("/update_data/<table>/<id>", methods=["GET", "POST"])
def update_data(table, id):
    if request.method == "POST":
        if table == "BOOKS":
            data = (
                request.form["field1"],
                request.form["field2"],
                request.form["field3"],
                request.form["field4"],
                request.form["field5"],
                id,
            )
            query = "UPDATE BOOKS SET BOOK_ID=%s, AUTHOR_NAME=%s, TITLE=%s, EDITION=%s, PRICE=%s WHERE BOOK_ID=%s"
        elif table == "PUBLISHER":
            data = (
                request.form["field1"],
                request.form["field2"],
                request.form["field3"],
                id,
            )
            query = "UPDATE PUBLISHER SET P_ID=%s, PNAME=%s, YOP=%s WHERE P_ID=%s"
        elif table == "PUBLISHES":
            data = (
                request.form["field1"],
                request.form["field2"],
                id,
            )
            query = (
                "UPDATE PUBLISHES SET BOOK_ID=%s, P_ID=%s WHERE BOOK_ID=%s AND P_ID=%s"
            )
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        return redirect(url_for("display_data", table=table))

    cnx = create_connection()
    cursor = cnx.cursor()

    if table == "BOOKS":
        query = "SELECT BOOK_ID, AUTHOR_NAME, TITLE, EDITION, PRICE FROM BOOKS WHERE BOOK_ID = %s"
    elif table == "PUBLISHER":
        query = "SELECT P_ID, PNAME, YOP FROM PUBLISHER WHERE P_ID = %s"
    elif table == "PUBLISHES":
        query = "SELECT BOOK_ID, P_ID FROM PUBLISHES WHERE BOOK_ID = %s AND P_ID = %s"

    cursor.execute(query, (id,))
    data = cursor.fetchone()
    cursor.close()
    return render_template("update_data.html", data=data, table=table)


if __name__ == "__main__":
    app.run(debug=True)
