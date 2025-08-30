-- Role Enum
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
        CREATE TYPE userrole AS ENUM ('patient', 'doctor', 'administrator');
    END IF;
END $$;

-- users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role userrole NOT NULL
);

-- services
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    clinic_name VARCHAR(255) NOT NULL,
    doctor_id INTEGER NOT NULL,
    CONSTRAINT fk_doctor FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE
);

-- appointments
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'booked' NOT NULL,
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_service FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);