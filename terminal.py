from functions import create_connection, insert_student_marks

while True:
    print("1. Insert student marks")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        usn = input("Enter USN: ")
        name = input("Enter name: ")
        age = input("Enter age: ")
        branch = input("Enter branch: ")
        total_marks = input("Enter total marks: ")

        connection = create_connection("localhost", "root", "password", "college")
        insert_student_marks(connection, usn, name, age, branch, total_marks)
    elif choice == "2":
        break
    else:
        print("Invalid choice. Please try again.")