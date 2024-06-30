from flask import *
from pharmacy.pharmacy import *
import json


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/enter")
def enter():
    return render_template("enter.html")


@app.route("/enter_data", methods=["POST"])
def web_enter_data():
    table = request.form["table"]
    # Initialize an empty list to hold the data values
    data_values = []
    # Iterate over all form fields, excluding the 'table' field
    for key in request.form:
        if key != "table":
            data_values.append(request.form[key])
    # Convert the list of values to a tuple
    data = tuple(data_values)
    db = connect_database()
    enter_data(db, table, data)
    db.close()
    return "Data entered successfully!"


@app.route("/display")
def display():
    tables = {
        "LOGIN": "LOGIN_USERNAME, USER_PASSWORD, LOGIN_ROLE_ID, LOGIN_ID",
        "USER": "USER_ID, USER_NAME, USER_MOBILE_NUMBER, USER_EMAIL, USER_ADDRESS",
        "MEDICINE": "M_NAME, M_ID, MEDICINE_TYPE, DOSAGE, COST, DESCRIPTION",
        "COMPANY": "C_NAME, C_ID, C_ADDRESS",
    }
    return render_template("display.html", tables=tables.keys())

@app.route("/display_data", methods=["POST"])
def web_display_data():
    table = request.form["table"]
    db = connect_database()
    data = display_data(db, table)
    db.close()

    headers = data[0].keys() if data else []
    rows = [list(row.values()) for row in data] if data else []

    return render_template("display_table.html", table=table, headers=headers, rows=rows)



@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/update_data", methods=["POST"])
def web_update_data():
    table = request.form.get("table")
    # Initialize an empty dictionary to collect data fields
    data_fields = {}
    # Iterate over all form fields
    for key in request.form:
        if key.startswith("data["):
            # Extract the actual field name from the key
            field_name = key[5:-1]  # Removes 'data[' prefix and ']' suffix
            data_fields[field_name] = request.form[key]

    if not data_fields:
        # Handle the case where no data fields are provided
        return "Missing data parameter", 400

    # Now, data_fields contains all the data inputs as a dictionary
    # Convert it to the desired format (e.g., a tuple of values) as needed for update_data
    data_values = tuple(data_fields.values())

    db = connect_database()
    update_data(db, table, data_values)
    db.close()
    return "Data updated successfully!"


@app.route("/delete")
def web_delete():
    return render_template("delete.html")


@app.route("/delete_data", methods=["POST"])
def Web_delete_data():
    table = request.form["table"]
    data = request.form["data"]
    data = tuple(data.split(","))
    db = connect_database()
    delete_data(db, table, data)
    db.close()
    # Return a small HTML page with JavaScript for the alert
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Deleted</title>
        <script type="text/javascript">
            alert("Data deleted successfully!");
            window.location.href = "/"; // Redirect back to the homepage or another page
        </script>
    </head>
    <body>
    </body>
    </html>
    """


@app.route("/search")
def web_search():
    return render_template("search_form.html")


@app.route("/search_data", methods=["POST"])
def web_search_data():
    table = request.form["table"]
    data = request.form["data"]
    data = tuple(data.split(","))
    db = connect_database()
    results = search_data(db, table, data)  # Assuming this returns a list of tuples representing rows
    db.close()
    # Render a template with the results
    return render_template("search_results.html", results=results, table=table)


if __name__ == "__main__":
    app.run(debug=True)
