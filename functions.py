import mysql.connector

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

    return connection

def insert_student_marks(connection, usn, name, age, branch, total_marks):
    cursor = connection.cursor()
    query = "INSERT INTO students (usn, name, age, branch, total_marks) VALUES (%s, %s, %s, %s, %s)"
    values = (usn, name, age, branch, total_marks)

    cursor.execute(query, values)
    connection.commit()

    print("Student marks inserted successfully.")