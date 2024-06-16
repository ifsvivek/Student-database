import mysql.connector
from prettytable import PrettyTable


def create_connection():
    cnx = mysql.connector.connect(
        user="root",
        password="Vinu@_07",
        host="localhost",
        database="library",
    )
    return cnx


def enter_data(cnx, table, data):
    cursor = cnx.cursor()
    if table == "BOOKS":
        query = "INSERT INTO BOOKS (BOOK_ID, AUTHOR_NAME, TITLE, EDITION, PRICE) VALUES (%s, %s, %s, %s, %s)"
    elif table == "PUBLISHER":
        query = "INSERT INTO PUBLISHER (P_ID, PNAME, YOP) VALUES (%s, %s, %s)"
    elif table == "PUBLISHES":
        query = "INSERT INTO PUBLISHES (BOOK_ID, P_ID) VALUES (%s, %s)"
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()


def display_data(cnx, table):
    cursor = cnx.cursor()
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    x = PrettyTable()
    x.field_names = [i[0] for i in cursor.description]

    for row in cursor:
        x.add_row(row)

    print(x)
    cursor.close()


def update_data(cnx, table, data):
    cursor = cnx.cursor()
    if table == "BOOKS":
        query = "UPDATE BOOKS SET AUTHOR_NAME = %s, TITLE = %s, EDITION = %s, PRICE = %s WHERE BOOK_ID = %s"
    elif table == "PUBLISHER":
        query = "UPDATE PUBLISHER SET PNAME = %s, YOP = %s WHERE P_ID = %s"
    elif table == "PUBLISHES":
        query = "UPDATE PUBLISHES SET P_ID = %s WHERE BOOK_ID = %s"
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()


def delete_data(cnx, table, data):
    cursor = cnx.cursor()
    if table == "BOOKS":
        query = "DELETE FROM BOOKS WHERE BOOK_ID = %s"
    elif table == "PUBLISHER":
        query = "DELETE FROM PUBLISHER WHERE P_ID = %s"
    elif table == "PUBLISHES":
        query = "DELETE FROM PUBLISHES WHERE BOOK_ID = %s"
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()


def search_data(cnx, table, data):
    cursor = cnx.cursor()
    if table == "BOOKS":
        query = "SELECT * FROM BOOKS WHERE BOOK_ID = %s"
    elif table == "PUBLISHER":
        query = "SELECT * FROM PUBLISHER WHERE P_ID = %s"
    elif table == "PUBLISHES":
        query = "SELECT * FROM PUBLISHES WHERE BOOK_ID = %s"
    cursor.execute(query, data)
    x = PrettyTable()
    x.field_names = [i[0] for i in cursor.description]

    for row in cursor:
        x.add_row(row)

    print(x)
    cursor.close()


# Usage
cnx = create_connection()

while True:
    try:
        print("1. Enter data")
        print("2. Display data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Search data")
        print("6. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            table = input("Enter table name: ")
            data = input("Enter data: ")
            data = tuple(data.split(","))
            enter_data(cnx, table, data)
        elif choice == 2:
            table = input("Enter table name: ")
            display_data(cnx, table)
        elif choice == 3:
            table = input("Enter table name: ")
            data = input("Enter data: ")
            data = tuple(data.split(","))
            update_data(cnx, table, data)
        elif choice == 4:
            table = input("Enter table name: ")
            data = input("Enter data: ")
            data = tuple(data.split(","))
            delete_data(cnx, table, data)
        elif choice == 5:
            table = input("Enter table name: ")
            data = input("Enter data: ")
            data = tuple(data.split(","))
            search_data(cnx, table, data)
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")


cnx.close()
