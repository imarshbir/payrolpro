
# Employee Dashboard - Backend (Flask + MongoDB)

This backend provides simple REST APIs for:
- Payroll management
- Salary slip update (draft & finalize)
- Job profile management
- Promotion management
- Simple chatbot endpoint (stub)

## Notes
- This project uses MongoDB as storage. The provided `.env` already contains your MongoDB URI.
- For production, **do not** commit `.env` with credentials. This was created per your request.
- To run locally (if you decide to run):
  1. Create a Python 3.10+ virtual environment
  2. `pip install -r requirements.txt`
  3. `python app.py`
