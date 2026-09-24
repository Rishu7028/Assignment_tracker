from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["student_tracker"]
students = db["students"]


@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not name or not email or not course:
        return jsonify({
            "error": "name, email and course are required"
        }), 400
    existing_student = students.find_one({"email": email})

    if existing_student:
        return jsonify({
            "error": "Email already exists"
        }), 409

    student = {
        "name": name,
        "email": email,
        "course": course,
        "assignments": []
    }

    result = students.insert_one(student)
    return jsonify({
        "message": "Student added successfully",
        "student_id": str(result.inserted_id)
    }), 201


@app.route("/students", methods=["GET"])
def get_students():
    all_students = []

    for student in students.find():
        student["_id"] = str(student["_id"])
        all_students.append(student)
    return jsonify(all_students), 200

