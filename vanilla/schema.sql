-- Hapus tabel jika sudah ada agar bisa dijalankan ulang
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS services_doctors;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS health_facilities;
DROP TABLE IF EXISTS users;

-- Tabel untuk pengguna
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('patient', 'doctor', 'administrator'))
);

-- Tabel untuk fasilitas kesehatan
CREATE TABLE health_facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT
);

-- Tabel untuk layanan medis
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    facility_id INTEGER NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES health_facilities (id)
);

-- Tabel penghubung antara dokter dan layanan (Many-to-Many)
CREATE TABLE services_doctors (
    service_id INTEGER,
    doctor_id INTEGER,
    PRIMARY KEY (service_id, doctor_id),
    FOREIGN KEY (service_id) REFERENCES services (id),
    FOREIGN KEY (doctor_id) REFERENCES users (id)
);

-- Tabel untuk appointment
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users (id),
    FOREIGN KEY (doctor_id) REFERENCES users (id),
    FOREIGN KEY (service_id) REFERENCES services (id)
);