from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

# app init
app = Flask(__name__)

# config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

# model
class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.String(10), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  phone = db.Column(db.String(15), nullable=False)
  course = db.Column(db.String(100), nullable=False)
  enrollment_date = db.Column(db.Date, nullable=False)
  city = db.Column(db.String(100), nullable=False)
  grade = db.Column(db.String(10), nullable=False)
  
# schema
class StudentSchema(ma.Schema):
  class Meta:
    model = Student
    fields = ["id","name","age","gender","email","phone","course","enrollment_date","city","grade"]
    load_instance = True
    
# schema instance
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# routes
@app.route("/")
def home():
  return jsonify({"message":"Home page"})

# get all students
@app.route("/students", methods=["GET"])
def get_all_students():
  students = Student.query.all()
  return students_schema.dump(students)

# get student
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
  student = Student.query.get(student_id)
  return student_schema.dump(student)

# add student
@app.route("/students", methods=["POST"])
def add_students():
  temp_data = request.get_json()
  data = student_schema.load(temp_data)
  data["enrollment_date"] = datetime.strptime(data["enrollment_date"], "%Y-%m-%d").date()
  student = Student(**data)
  db.session.add(student)
  db.session.commit()
  return jsonify({"message":"student added successfully"})

# update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
  data = request.get_json()
  student = Student.query.get(student_id)
  student.name = data.get("name") or student.name
  student.age = data.get("age") or student.age
  student.gender = data.get("gender") or student.gender
  student.email = data.get("email") or student.email
  student.phone = data.get("phone") or student.phone
  student.course = data.get("course") or student.course
  if data.get("enrollment_date"):
    student.enrollment_date = datetime.strptime(data.get("enrollment_date"), "%Y-%m-%d").date()
  student.city = data.get("city") or student.city
  student.grade = data.get("grade") or student.grade
  db.session.commit()
  return jsonify({"message":"student updated successfully"})

# delete student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
  student = Student.query.get(student_id)
  db.session.delete(student)
  db.session.commit()
  return jsonify({"message":"student deleted successfully"})
  
# add/import students from excel file
@app.route("/students/import", methods=["POST"])
def import_students():
  return jsonify({"message":"excel file imported successfully"})

# app run
if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    
  app.run(debug=True)