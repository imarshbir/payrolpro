from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------
#  Dummy IT Department User
# ---------------------------------------------------------------------
users = [
    {
        "email": "itdept@gov.in",
        "password": "it123",
        "name": "IT Officer",
        "department": "IT"
    }
]

# ---------------------------------------------------------------------
#  Dummy Data: Employee Records
# ---------------------------------------------------------------------
employee_records = [
    {
        "id": 1,
        "name": "Arshbir Singh",
        "designation": "Junior Engineer",
        "department": "Mechanical",
        "joining_date": "2019-07-10"
    },
    {
        "id": 2,
        "name": "Simran Kaur",
        "designation": "Senior Clerk",
        "department": "Accounts",
        "joining_date": "2017-03-22"
    },
    {
        "id": 3,
        "name": "Rohit Verma",
        "designation": "Assistant",
        "department": "IT",
        "joining_date": "2018-12-05"
    }
]

# ---------------------------------------------------------------------
#  Dummy Payroll Data
# ---------------------------------------------------------------------
payrolls = [
    {"id": 1, "month": "Jan 2024", "employee": "Arshbir Singh", "salary": 42000, "deductions": 2000},
    {"id": 2, "month": "Jan 2024", "employee": "Simran Kaur", "salary": 38000, "deductions": 1500},
    {"id": 3, "month": "Jan 2024", "employee": "Rohit Verma", "salary": 45000, "deductions": 2300}
]

# ---------------------------------------------------------------------
#  Dummy Leave Module Data
# ---------------------------------------------------------------------
leaves = [
    {"id": 1, "employee": "Arshbir", "days": 2, "type": "Casual Leave", "status": "Approved"},
    {"id": 2, "employee": "Simran", "days": 5, "type": "Sick Leave", "status": "Pending"},
    {"id": 3, "employee": "Rohit", "days": 1, "type": "Casual Leave", "status": "Approved"},
]

# ---------------------------------------------------------------------
#  Dummy Transfer Data
# ---------------------------------------------------------------------
transfers = [
    {"id": 1, "employee": "Arshbir", "from": "Ludhiana", "to": "Patiala", "date": "2022-03-10"},
    {"id": 2, "employee": "Simran", "from": "Chandigarh", "to": "Delhi", "date": "2021-09-15"},
]

# ---------------------------------------------------------------------
#  Dummy Promotion Data
# ---------------------------------------------------------------------
promotions = [
    {"id": 1, "employee": "Arshbir", "old_post": "Junior Engineer", "new_post": "Engineer", "year": 2023},
    {"id": 2, "employee": "Rohit", "old_post": "Assistant", "new_post": "Senior Assistant", "year": 2022},
]

# ---------------------------------------------------------------------
#  LOGIN API
# ---------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "message": "Login successful",
                "role": user["department"],
                "name": user["name"]
            })

    return jsonify({"error": "Invalid email or password"}), 401


# ---------------------------------------------------------------------
#  API: Employee Records
# ---------------------------------------------------------------------
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employee_records)


# ---------------------------------------------------------------------
#  API: Payrolls
# ---------------------------------------------------------------------
@app.route("/payrolls", methods=["GET"])
def get_payrolls():
    return jsonify(payrolls)


# ---------------------------------------------------------------------
#  API: Leave Module
# ---------------------------------------------------------------------
@app.route("/leaves", methods=["GET"])
def get_leaves():
    return jsonify(leaves)


# ---------------------------------------------------------------------
#  API: Transfers
# ---------------------------------------------------------------------
@app.route("/transfers", methods=["GET"])
def get_transfers():
    return jsonify(transfers)


# ---------------------------------------------------------------------
#  API: Promotions
# ---------------------------------------------------------------------
@app.route("/promotions", methods=["GET"])
def get_promotions():
    return jsonify(promotions)


# ---------------------------------------------------------------------
#  RUN
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
