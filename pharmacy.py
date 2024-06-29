import mysql.connector
from prettytable import PrettyTable


def connect_database():
    db = mysql.connector.connect(
        user="root",
        password="1234",
        host="localhost",
        database="dbms",
    )
    return db


import logging


def enter_data(db, table, data):
    cursor = db.cursor()
    try:
        # Dynamically construct the column names and placeholders based on the length of 'data'
        columns = {
            "LOGIN": "LOGIN_USERNAME, USER_PASSWORD, LOGIN_ROLE_ID, LOGIN_ID",
            "USER": "USER_ID, USER_NAME, USER_MOBILE_NUMBER, USER_EMAIL, USER_ADDRESS",
            "MEDICINE": "M_NAME, M_ID, MEDICINE_TYPE, DOSAGE, COST, DESCRIPTION",
            "COMPANY": "C_NAME, C_ID, C_ADDRESS",
        }

        if table not in columns:
            raise ValueError(f"Unexpected table name: {table}")

        placeholders = ", ".join(
            ["%s"] * len(data)
        )  # Corrected to use the length of the tuple
        query = f"INSERT INTO {table}({columns[table]}) VALUES({placeholders})"

        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback in case of error
        logging.error(f"Error inserting data into {table}: {e}")
        raise
    finally:
        cursor.close()


def display_data(db, table):
    cursor = db.cursor()
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    t = PrettyTable()
    t.field_names = [i[0] for i in cursor.description]

    data = []
    for row in cursor:
        row_data = {}
        for i, col in enumerate(cursor.description):
            row_data[col[0]] = row[i]
        data.append(row_data)

    cursor.close()
    return data


def update_data(db, table, data):
    cursor = db.cursor()
    try:
        columns = {
            "LOGIN": (
                "LOGIN_USERNAME=%s, USER_PASSWORD=%s, LOGIN_ROLE_ID=%s",
                "LOGIN_ID=%s",
            ),
            "USER": (
                "USER_NAME=%s, USER_MOBILE_NUMBER=%s, USER_EMAIL=%s, USER_ADDRESS=%s",
                "USER_ID=%s",
            ),
            "MEDICINE": (
                "M_NAME=%s, MEDICINE_TYPE=%s, DOSAGE=%s, COST=%s, DESCRIPTION=%s",
                "M_ID=%s",
            ),
            "COMPANY": ("C_NAME=%s, C_ADDRESS=%s", "C_ID=%s"),
        }

        if table not in columns:
            raise ValueError(f"Unexpected table name: {table}")

        set_clause, where_clause = columns[table]
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        # Log the query and data for debugging
        logging.debug(f"Executing query: {query}")
        logging.debug(f"With data: {data}")

        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating data in {table}: {e}")
        raise
    finally:
        cursor.close()


def delete_data(db, table, data):
    cursor = db.cursor()
    if table == "LOGIN":
        query = "DELETE FROM LOGIN WHERE LOGIN_ID=%s"
    elif table == "USER":
        query = "DELETE FROM USER WHERE USER_ID=%s"
    elif table == "MEDICINE":
        query = "DELETE FROM MEDICINE WHERE M_ID=%s"
    elif table == "COMPANY":
        query = "DELETE FROM COMPANY WHERE C_ID=%s"
    cursor.execute(query, data)
    db.commit()
    cursor.close()


def search_data(db, table, data):
    cursor = db.cursor()
    query = ""
    if table == "LOGIN":
        query = "SELECT * FROM LOGIN WHERE LOGIN_ID=%s"
    elif table == "USER":
        query = "SELECT * FROM USER WHERE USER_ID=%s"
    elif table == "MEDICINE":
        query = "SELECT * FROM MEDICINE WHERE M_ID=%s"
    elif table == "COMPANY":
        query = "SELECT * FROM COMPANY WHERE C_ID=%s"
    cursor.execute(query, data)

    # Fetch all rows from cursor
    rows = cursor.fetchall()

    # Get column headers
    columns = [i[0] for i in cursor.description]

    # Convert rows and columns to a list of dictionaries
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    return results
