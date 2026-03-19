from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age, "grade": self.grade}


with app.app_context():
    db.create_all()


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "age", "grade")):
        return jsonify({"error": "name, age, and grade are required"}), 400
    student = Student(name=data["name"], age=data["age"], grade=data["grade"])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict())


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json()
    if "name" in data:
        student.name = data["name"]
    if "age" in data:
        student.age = data["age"]
    if "grade" in data:
        student.grade = data["grade"]
    db.session.commit()
    return jsonify(student.to_dict())


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"})


if __name__ == "__main__":
    app.run(debug=True)
