import sqlite3
import bcrypt
from datetime import datetime, timedelta

DB_NAME = 'healthlinkr.db'

# Hapus DB lama jika ada
import os
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

# Fungsi untuk hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Koneksi ke DB dan jalankan schema.sql
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

with open('schema.sql', 'r') as f:
    cursor.executescript(f.read())
print("Database schema created.")

# --- Insert Data Dummy ---

try:
    # Users
    users_to_add = [
        ('admin', 'admin@health.com', hash_password('admin123'), 'administrator'),
        ('dr.budi', 'budi@health.com', hash_password('dokter123'), 'doctor'),
        ('dr.susan', 'susan@health.com', hash_password('dokter123'), 'doctor'),
        ('andi', 'andi@mail.com', hash_password('pasien123'), 'patient'),
        ('citra', 'citra@mail.com', hash_password('pasien123'), 'patient')
    ]
    cursor.executemany("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)", users_to_add)
    print(f"{cursor.rowcount} users created.")

    # Health Facilities
    facilities_to_add = [
        ('RS Sehat Selalu', 'Jl. Kesehatan No. 1, Jakarta'),
        ('Klinik Ceria', 'Jl. Bahagia No. 2, Jakarta')
    ]
    cursor.executemany("INSERT INTO health_facilities (name, address) VALUES (?, ?)", facilities_to_add)
    print(f"{cursor.rowcount} facilities created.")

    # Services
    services_to_add = [
        ('Konsultasi Umum', 'Pemeriksaan kesehatan umum', 1), # di RS Sehat Selalu
        ('Konsultasi Gigi', 'Pemeriksaan gigi dan mulut', 2)  # di Klinik Ceria
    ]
    cursor.executemany("INSERT INTO services (name, description, facility_id) VALUES (?, ?, ?)", services_to_add)
    print(f"{cursor.rowcount} services created.")

    # Assign doctors to services
    # dr.budi (id=2) -> Konsultasi Umum (id=1)
    # dr.susan (id=3) -> Konsultasi Gigi (id=2)
    services_doctors_to_add = [(1, 2), (2, 3)]
    cursor.executemany("INSERT INTO services_doctors (service_id, doctor_id) VALUES (?, ?)", services_doctors_to_add)
    print(f"{cursor.rowcount} doctor assignments created.")
    
    # Appointments
    # andi (id=4) dengan dr.budi (id=2) untuk Konsultasi Umum (id=1)
    appointment_time = (datetime.now() + timedelta(days=3)).isoformat()
    appointments_to_add = [(4, 2, 1, appointment_time, 'scheduled')]
    cursor.executemany("INSERT INTO appointments (patient_id, doctor_id, service_id, appointment_time, status) VALUES (?, ?, ?, ?, ?)", appointments_to_add)
    print(f"{cursor.rowcount} appointments created.")

    conn.commit()
    print("Dummy data inserted successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()
finally:
    conn.close()