# ---------------------------------------------------------
# Student Database Application
# COMP / Database Application Assignment
#
# This application connects to a PostgreSQL database and
# performs CRUD operations on the students table.
#
# CRUD:
# Create - Add a new student
# Read   - Display all students
# Update - Change a student's email
# Delete - Remove a student
# ---------------------------------------------------------

import os
from datetime import date

import psycopg
from dotenv import load_dotenv


# Load database credentials from the .env file.
load_dotenv()


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

def getConnection():
    """
    Establishes and returns a connection to PostgreSQL.

    Database credentials are retrieved from the .env file.
    """
    
    return psycopg.connect(
        dbname="student_database",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


# ---------------------------------------------------------
# Function 1: Get All Students
# ---------------------------------------------------------

def getAllStudents():
    """
    Retrieves all student records from the database
    and displays them.
    """

    print("\n========== ALL STUDENTS ==========")

    try:
        # Connect to the PostgreSQL database.
        with getConnection() as conn:

            # Create a cursor to execute SQL statements.
            with conn.cursor() as cursor:

                # Retrieve all students, ordered by student ID.
                cursor.execute("""
                    SELECT student_id, first_name, last_name,
                           email, enrollment_date
                    FROM students
                    ORDER BY student_id;
                """)

                # Retrieve all results.
                students = cursor.fetchall()

                # Display the records.
                if not students:
                    print("No students found in the database.")

                else:
                    for student in students:
                        print("----------------------------------")
                        print(f"Student ID:       {student[0]}")
                        print(f"First Name:       {student[1]}")
                        print(f"Last Name:        {student[2]}")
                        print(f"Email:            {student[3]}")
                        print(f"Enrollment Date:  {student[4]}")

                    print("----------------------------------")

    except psycopg.Error as error:
        print(f"Database error: {error}")


# ---------------------------------------------------------
# Function 2: Add Student
# ---------------------------------------------------------

def addStudent(first_name, last_name, email, enrollment_date):
    """
    Inserts a new student into the students table.

    Parameters:
        first_name: Student's first name
        last_name: Student's last name
        email: Student's unique email address
        enrollment_date: Student's enrollment date
    """

    try:
        # Convert the date string into a Python date object.
        if enrollment_date:
            enrollment_date = date.fromisoformat(enrollment_date)
        else:
            enrollment_date = None

        # Connect to the database.
        with getConnection() as conn:

            with conn.cursor() as cursor:

                # Insert the new student.
                # The student_id is automatically generated.
                cursor.execute("""
                    INSERT INTO students
                    (first_name, last_name, email, enrollment_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING student_id;
                """, (first_name, last_name, email, enrollment_date))

                # Retrieve the automatically generated ID.
                new_id = cursor.fetchone()[0]

                print("\nStudent successfully added!")
                print(f"New Student ID: {new_id}")

    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD.")

    except psycopg.errors.UniqueViolation:
        print("Error: This email address is already registered.")

    except psycopg.Error as error:
        print(f"Database error: {error}")


# ---------------------------------------------------------
# Function 3: Update Student Email
# ---------------------------------------------------------

def updateStudentEmail(student_id, new_email):
    """
    Updates the email address of an existing student.

    Parameters:
        student_id: ID of the student to update
        new_email: New email address
    """

    try:
        # Connect to the database.
        with getConnection() as conn:

            with conn.cursor() as cursor:

                # Update the student's email address.
                cursor.execute("""
                    UPDATE students
                    SET email = %s
                    WHERE student_id = %s;
                """, (new_email, student_id))

                # Check whether a student was updated.
                if cursor.rowcount > 0:
                    print("\nStudent email successfully updated!")

                else:
                    print("\nNo student found with that ID.")

    except psycopg.errors.UniqueViolation:
        print("Error: This email address is already registered.")

    except psycopg.Error as error:
        print(f"Database error: {error}")


# ---------------------------------------------------------
# Function 4: Delete Student
# ---------------------------------------------------------

def deleteStudent(student_id):
    """
    Deletes a student record from the database.

    Parameters:
        student_id: ID of the student to delete
    """

    try:
        # Connect to the database.
        with getConnection() as conn:

            with conn.cursor() as cursor:

                # Delete the student with the specified ID.
                cursor.execute("""
                    DELETE FROM students
                    WHERE student_id = %s;
                """, (student_id,))

                # Check whether a student was deleted.
                if cursor.rowcount > 0:
                    print("\nStudent successfully deleted!")

                else:
                    print("\nNo student found with that ID.")

    except psycopg.Error as error:
        print(f"Database error: {error}")


# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------

def main():
    """
    Displays the application menu and allows the user
    to select different database operations.
    """

    while True:

        print("\n===================================")
        print("       STUDENT DATABASE SYSTEM")
        print("===================================")
        print("1. Display All Students")
        print("2. Add Student")
        print("3. Update Student Email")
        print("4. Delete Student")
        print("0. Exit")
        print("===================================")

        choice = input("Enter your choice: ").strip()

        # Option 1: Display all students.
        if choice == "1":
            getAllStudents()

        # Option 2: Add a new student.
        elif choice == "2":

            print("\n========== ADD STUDENT ==========")

            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            email = input("Enter email: ").strip()
            enrollment_date = input(
                "Enter enrollment date (YYYY-MM-DD), "
                "or leave blank: "
            ).strip()

            # Ensure required fields are provided.
            if not first_name or not last_name or not email:
                print("First name, last name, and email are required.")

            else:
                addStudent(
                    first_name,
                    last_name,
                    email,
                    enrollment_date
                )

        # Option 3: Update a student's email.
        elif choice == "3":

            print("\n========== UPDATE EMAIL ==========")

            try:
                student_id = int(input("Enter student ID: "))
                new_email = input("Enter new email: ").strip()

                if not new_email:
                    print("Email cannot be empty.")
                else:
                    updateStudentEmail(student_id, new_email)

            except ValueError:
                print("Please enter a valid student ID.")

        # Option 4: Delete a student.
        elif choice == "4":

            print("\n========== DELETE STUDENT ==========")

            try:
                student_id = int(input("Enter student ID: "))
                deleteStudent(student_id)

            except ValueError:
                print("Please enter a valid student ID.")

        # Option 0: Exit the application.
        elif choice == "0":
            print("\nThank you for using the Student Database System!")
            break

        # Handle invalid menu choices.
        else:
            print("\nInvalid choice. Please try again.")


# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()