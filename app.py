from flask import Flask, render_template, request, redirect, url_for

from database import DatabaseManager


app = Flask(__name__)

db = DatabaseManager()


# -------------------------
# Dashboard / View Students
# -------------------------

@app.route("/")
def home():

    search = request.args.get("search", "").strip()

    if search:
        students = db.search_students(search)
    else:
        students = db.get_all_students()

    total_students = db.get_student_count()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        search=search
    )


# -------------------------
# Add Student
# -------------------------

@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()
    course = request.form["course"].strip()
    marks = request.form["marks"].strip()

    if not name or not email or not course or not marks:
        return redirect(url_for("home"))

    db.add_student(
        name,
        email,
        phone,
        course,
        marks
    )

    return redirect(url_for("home"))


# -------------------------
# Edit Student
# -------------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        course = request.form["course"].strip()
        marks = request.form["marks"].strip()

        db.update_student(
            id,
            name,
            email,
            phone,
            course,
            marks
        )

        return redirect(url_for("home"))

    student = db.get_student(id)

    return render_template(
        "edit.html",
        student=student
    )


# -------------------------
# Delete Student
# -------------------------

@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):

    db.delete_student(id)

    return redirect(url_for("home"))


# -------------------------
# Run Application
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)