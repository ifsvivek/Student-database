from flask import Flask, request, redirect, render_template
import mysql.connector

app = Flask(__name__)


def connect_database():
    return mysql.connector.connect(
        user="root", password="1234", host="localhost", database="appy"
    )


@app.route("/")
def index():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM championship")
    teams = cursor.fetchall()
    db.close()
    return render_template("champ.html", teams=teams)


@app.route("/add", methods=["POST"])
def add_team():
    team_name = request.form["team_name"]
    team_coach = request.form["team_coach"]
    captain = request.form["captain"]
    total_players = request.form["total_players"]
    interest = request.form["interest"]
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO championship (team_name, team_coach, captain, total_players, interest) VALUES (%s, %s, %s, %s, %s)",
        (team_name, team_coach, captain, total_players, interest),
    )
    db.commit()
    db.close()
    return redirect("/")


@app.route("/update/<int:team_id>", methods=["POST"])
def update_team(team_id):
    team_name = request.form["team_name"]
    team_coach = request.form["team_coach"]
    captain = request.form["captain"]
    total_players = request.form["total_players"]
    interest = request.form["interest"]
    db = connect_database()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE championship SET team_name=%s, team_coach=%s, captain=%s, total_players=%s, interest=%s WHERE team_id=%s",
        (team_name, team_coach, captain, total_players, interest, team_id),
    )
    db.commit()
    db.close()
    return redirect("/")


@app.route("/delete/<int:team_id>")
def delete_team(team_id):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM championship WHERE team_id=%s", (team_id,))
    db.commit()
    db.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
