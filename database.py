import mysql.connector
import os

from dotenv import load_dotenv


# Load .env from the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


class DatabaseManager:

    def __init__(self):
       self.db = mysql.connector.connect(
    host=os.environ["MYSQL_HOST"],
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DATABASE"]
)

    # -------------------------
    # Get All Students
    # -------------------------

    def get_all_students(self):

        cursor = self.db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students")

        students = cursor.fetchall()

        cursor.close()

        return students

    # -------------------------
    # Add Student
    # -------------------------

    def add_student(self, name, email, phone, course, marks):

        cursor = self.db.cursor()

        query = """
            INSERT INTO students
            (name, email, phone, course, marks)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            email,
            phone,
            course,
            marks
        )

        cursor.execute(query, values)

        self.db.commit()

        cursor.close()

    # -------------------------
    # Get One Student
    # -------------------------

    def get_student(self, student_id):

        cursor = self.db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        cursor.close()

        return student

    # -------------------------
    # Update Student
    # -------------------------

    def update_student(
        self,
        student_id,
        name,
        email,
        phone,
        course,
        marks
    ):

        cursor = self.db.cursor()

        query = """
            UPDATE students
            SET name = %s,
                email = %s,
                phone = %s,
                course = %s,
                marks = %s
            WHERE id = %s
        """

        values = (
            name,
            email,
            phone,
            course,
            marks,
            student_id
        )

        cursor.execute(query, values)

        self.db.commit()

        cursor.close()

    # -------------------------
    # Delete Student
    # -------------------------

    def delete_student(self, student_id):

        cursor = self.db.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        self.db.commit()

        cursor.close()

    # -------------------------
    # Search Students
    # -------------------------

    def search_students(self, search):

        cursor = self.db.cursor(dictionary=True)

        query = """
            SELECT * FROM students
            WHERE name LIKE %s
               OR email LIKE %s
               OR course LIKE %s
        """

        search_value = f"%{search}%"

        cursor.execute(
            query,
            (
                search_value,
                search_value,
                search_value
            )
        )

        students = cursor.fetchall()

        cursor.close()

        return students

    # -------------------------
    # Get Student Count
    # -------------------------

    def get_student_count(self):

        cursor = self.db.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        count = cursor.fetchone()[0]

        cursor.close()

        return count