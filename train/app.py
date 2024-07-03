from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="appy"
)
cursor = db.cursor()


@app.route("/")
def index():
    cursor.execute("SELECT * FROM Train")
    trains = cursor.fetchall()
    return render_template("index.html", trains=trains)


@app.route("/add", methods=["POST", "GET"])
def add_train():
    if request.method == "POST":
        name = request.form["name"]
        cost = request.form["cost"]
        distance = request.form["distance"]
        date = request.form["date"]

        sql = "INSERT INTO Train (Name, Cost, Distance, Date) VALUES (%s, %s, %s, %s)"
        val = (name, cost, distance, date)
        cursor.execute(sql, val)
        db.commit()
        return redirect(url_for("index"))
    else:
        return render_template("add.html")


@app.route("/update/<int:id>", methods=["GET"])
def update_train(id):
    cursor.execute("SELECT * FROM Train WHERE id = %s", (id,))
    train = cursor.fetchone()
    return render_template("update.html", train=train)


@app.route("/update/<int:id>", methods=["POST"])
def update_train_post(id):
    name = request.form["name"]
    cost = request.form["cost"]
    distance = request.form["distance"]
    date = request.form["date"]

    sql = "UPDATE Train SET Name=%s, Cost=%s, Distance=%s, Date=%s WHERE id=%s"
    val = (name, cost, distance, date, id)
    cursor.execute(sql, val)
    db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_train(id):
    sql = "DELETE FROM Train WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
