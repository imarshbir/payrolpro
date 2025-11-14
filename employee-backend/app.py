
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in environment")

client = MongoClient(MONGO_URI)
db = client.get_database()  # uses default DB from URI

app = Flask(__name__)
CORS(app)

# Collections
employees_col = db.get_collection("employees")
payroll_col = db.get_collection("monthly_payrolls")
salary_drafts_col = db.get_collection("salary_slip_drafts")
promotions_col = db.get_collection("promotions")
profiles_col = db.get_collection("job_profiles")
chat_col = db.get_collection("chat_history")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status":"ok"})

# Employees CRUD (simplified)
@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error":"Missing 'name'"}), 400
    res = employees_col.insert_one(data)
    return jsonify({"_id": str(res.inserted_id)}), 201

@app.route('/api/employees/<id>', methods=['GET'])
def get_employee(id):
    emp = employees_col.find_one({"_id": ObjectId(id)})
    if not emp:
        return jsonify({"error":"Not found"}), 404
    emp['_id'] = str(emp['_id'])
    return jsonify(emp)

# Payroll generation (basic)
# Expected JSON: { "employee_id": "<id>", "month": "YYYY-MM", "components": {"basic":..., "allowances":..., "deductions":...} }
@app.route('/api/payroll/generate', methods=['POST'])
def generate_payroll():
    data = request.json
    required = ['employee_id','month','components']
    if not data or not all(k in data for k in required):
        return jsonify({"error":"Missing fields"}), 400

    comp = data['components']
    gross = comp.get('basic',0) + comp.get('allowances',0)
    net = gross - comp.get('deductions',0)
    doc = {
        "employee_id": data['employee_id'],
        "month": data['month'],
        "components": comp,
        "gross": gross,
        "net": net,
        "locked": False
    }
    res = payroll_col.insert_one(doc)
    doc['_id'] = str(res.inserted_id)
    return jsonify(doc), 201

@app.route('/api/payroll/<pid>/lock', methods=['POST'])
def lock_payroll(pid):
    payroll_col.update_one({"_id": ObjectId(pid)}, { "$set": { "locked": True } })
    return jsonify({"status":"locked"})

# Salary slip drafts & finalize
@app.route('/api/salary/draft', methods=['POST'])
def create_salary_draft():
    data = request.json
    if not data or 'employee_id' not in data:
        return jsonify({"error":"Missing 'employee_id'"}),400
    data['status'] = 'draft'
    res = salary_drafts_col.insert_one(data)
    return jsonify({"_id": str(res.inserted_id)}), 201

@app.route('/api/salary/draft/<id>', methods=['PUT'])
def update_salary_draft(id):
    data = request.json
    salary_drafts_col.update_one({"_id": ObjectId(id)}, { "$set": data })
    return jsonify({"status":"updated"})

@app.route('/api/salary/finalize/<id>', methods=['POST'])
def finalize_salary(id):
    draft = salary_drafts_col.find_one({"_id": ObjectId(id)})
    if not draft:
        return jsonify({"error":"Draft not found"}),404
    doc = draft.copy()
    doc['status'] = 'final'
    res = payroll_col.insert_one(doc)
    salary_drafts_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"_id":str(res.inserted_id)}),201

# Job profile
@app.route('/api/profile/<employee_id>', methods=['PUT'])
def update_profile(employee_id):
    data = request.json
    profiles_col.update_one({"employee_id": employee_id}, { "$set": data }, upsert=True)
    return jsonify({"status":"profile_updated"})

@app.route('/api/profile/<employee_id>', methods=['GET'])
def get_profile(employee_id):
    prof = profiles_col.find_one({"employee_id": employee_id})
    if not prof:
        return jsonify({"error":"not found"}),404
    prof['_id']=str(prof['_id'])
    return jsonify(prof)

# Promotions
@app.route('/api/promotion/apply', methods=['POST'])
def apply_promotion():
    data = request.json
    if not data or 'employee_id' not in data or 'new_designation' not in data:
        return jsonify({"error":"Missing fields"}),400
    data['applied_at'] = __import__('datetime').datetime.utcnow()
    res = promotions_col.insert_one(data)
    profiles_col.update_one({"employee_id": data['employee_id']}, { "$set": { "designation": data['new_designation'] } }, upsert=True)
    return jsonify({"_id":str(res.inserted_id)}),201

# Chatbot (simple rule-based stub)
@app.route('/api/chat', methods=['POST'])
def chat():
    # Expected payload: { "employee_id": "...", "message": "..." }
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error":"Missing 'message'"}),400
    msg = data['message'].lower()
    reply = "I'm sorry, I don't understand. Contact HR."
    if 'leave' in msg:
        reply = "To apply leave, go to Leave Module > Apply. Your balance is X days (mock)."
    elif 'salary' in msg:
        reply = "Salary slips are under Salary Slip section. You can request an update."
    record = { "employee_id": data.get('employee_id'), "message": data['message'], "reply": reply, "ts": __import__('datetime').datetime.utcnow() }
    inserted = chat_col.insert_one(record)
    record['_id'] = str(inserted.inserted_id)
    return jsonify(record)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
