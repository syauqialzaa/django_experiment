from flask import Flask, request, jsonify
import sqlite3
import bcrypt
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'healthlinkr.db'

# Fungsi helper untuk koneksi database
def get_db_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Memungkinkan akses kolom via nama
    return conn

# Helper untuk check password
def check_password(hashed_password, plain_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# --- Brief 1: Authentication & Authorization ---

# GET /api/login/ (Catatan: Seharusnya POST, tapi mengikuti brief)
@app.route('/api/login/', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_conn()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password(user['password_hash'], password):
        # Di aplikasi nyata, Anda akan membuat token (JWT) di sini
        return jsonify({"message": "Login successful", "user_id": user['id'], "role": user['role']}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# POST /api/signup/
@app.route('/api/signup/', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'patient')

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_conn()
        conn.execute(
            'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
            (username, email, hashed_password, role)
        )
        conn.commit()
        user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return jsonify({"message": "User created", "user_id": user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 409


# GET, PUT, DELETE /api/user/{user_id}/ (Gabungan /update)
@app.route('/api/user/<int:user_id>/', methods=['GET'])
@app.route('/api/user/<int:user_id>/update', methods=['PUT', 'DELETE'])
def user_detail(user_id):
    conn = get_db_conn()
    if request.method == 'GET':
        user = conn.execute('SELECT id, username, email, role FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(dict(user))

    elif request.method == 'PUT':
        data = request.get_json()
        # Update hanya field yang ada di request
        fields = {k: v for k, v in data.items() if k in ['username', 'email']}
        if not fields:
            return jsonify({"error": "No fields to update"}), 400
        
        set_clause = ", ".join([f"{key} = ?" for key in fields])
        values = list(fields.values()) + [user_id]
        
        conn.execute(f'UPDATE users SET {set_clause} WHERE id = ?', tuple(values))
        conn.commit()
        return jsonify({"message": "User updated"}), 200

    elif request.method == 'DELETE':
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return jsonify({"message": "User deleted"}), 200
    
    conn.close()

# --- Brief 2: Service Management ---

@app.route('/api/services/', methods=['GET', 'POST'])
def handle_services():
    conn = get_db_conn()
    if request.method == 'GET':
        query = """
            SELECT s.id, s.name, s.description, hf.name as facility_name,
                   GROUP_CONCAT(u.username) as doctors
            FROM services s
            JOIN health_facilities hf ON s.facility_id = hf.id
            LEFT JOIN services_doctors sd ON s.id = sd.service_id
            LEFT JOIN users u ON sd.doctor_id = u.id AND u.role = 'doctor'
            GROUP BY s.id
        """
        services = conn.execute(query).fetchall()
        return jsonify([dict(row) for row in services])

    elif request.method == 'POST':
        # Implementasi POST untuk tambah service
        return jsonify({"message": "Endpoint not implemented"}), 501
    conn.close()

# --- Brief 3: Appointment ---

@app.route('/api/appointments/', methods=['GET'])
def get_appointments():
    conn = get_db_conn()
    query = """
        SELECT a.id, p.username as patient, d.username as doctor, s.name as service, a.appointment_time, a.status
        FROM appointments a
        JOIN users p ON a.patient_id = p.id
        JOIN users d ON a.doctor_id = d.id
        JOIN services s ON a.service_id = s.id
    """
    appointments = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in appointments])

@app.route('/api/appointments/book/', methods=['POST'])
def book_appointment():
    # Implementasi untuk booking
    return jsonify({"message": "Endpoint not implemented"}), 501

@app.route('/api/appointments/<int:appointment_id>/cancel/', methods=['POST'])
def cancel_appointment(appointment_id):
    conn = get_db_conn()
    conn.execute("UPDATE appointments SET status = 'cancelled' WHERE id = ?", (appointment_id,))
    conn.commit()
    if conn.total_changes == 0:
        return jsonify({"error": "Appointment not found"}), 404
    conn.close()
    return jsonify({"message": "Appointment cancelled"}), 200


if __name__ == '__main__':
    app.run(debug=True)