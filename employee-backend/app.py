from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"
CORS(app, supports_credentials=True)

# ---------------------- DATABASE ----------------------
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database()

employees = db.employees
payrolls = db.payrolls
leaves = db.leaves
transfers = db.transfers
promotions = db.promotions
users = db.users

# ---------------------- SEED SAMPLE DATA ----------------------
def seed_data():
    if employees.count_documents({}) == 0:
        employees.insert_many([
            {
                "name": "Amit Kumar",
                "email": "amit@hrms.com",
                "department": "IT",
                "salary": 50000,
                "employee_id": "EMP001"
            },
            {
                "name": "Priya Sharma",
                "email": "priya@hrms.com",
                "department": "Finance",
                "salary": 62000,
                "employee_id": "EMP002"
            }
        ])

    if payrolls.count_documents({}) == 0:
        payrolls.insert_many([
            {"employee_id": "EMP001", "month": "Jan", "net_salary": 48000},
            {"employee_id": "EMP002", "month": "Jan", "net_salary": 60000},
        ])

    if leaves.count_documents({}) == 0:
        leaves.insert_many([
            {"employee_id": "EMP001", "days": 5, "type": "Sick Leave"},
            {"employee_id": "EMP002", "days": 2, "type": "Casual Leave"},
        ])

    if transfers.count_documents({}) == 0:
        transfers.insert_many([
            {"employee_id": "EMP001", "from": "Lucknow", "to": "Kanpur"},
        ])

    if promotions.count_documents({}) == 0:
        promotions.insert_many([
            {"employee_id": "EMP002", "old_role": "Junior Accountant", "new_role": "Senior Accountant"},
        ])

    if users.count_documents({}) == 0:
        users.insert_one({
            "email": "it@hrms.com",
            "password": "123",
            "role": "IT"
        })

seed_data()

# ---------------------- AUTH ----------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"], "password": data["password"]})

    if not user:
        return jsonify({"success": False, "message": "Invalid login"})

    session["role"] = user["role"]
    return jsonify({"success": True, "role": user["role"]})


# middleware
def require_login():
    if "role" not in session:
        return False
    return True

# ---------------------- PROTECTED ROUTES ----------------------
@app.route("/employees/all")
def get_employees():
    if not require_login():
        return jsonify({"error": "Login required"}), 401
    data = list(employees.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/payroll/all")
def get_payroll():
    if not require_login():
        return jsonify({"error": "Login required"}), 401
    data = list(payrolls.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/leaves/all")
def get_leaves():
    if not require_login():
        return jsonify({"error": "Login required"}), 401
    data = list(leaves.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/transfers/all")
def get_transfers():
    if not require_login():
        return jsonify({"error": "Login required"}), 401
    data = list(transfers.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/promotions/all")
def get_promotions():
    if not require_login():
        return jsonify({"error": "Login required"}), 401
    data = list(promotions.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/")
def home():
    return jsonify({"message": "Backend running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
