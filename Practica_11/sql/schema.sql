CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    photo TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    appointment_time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled','completed','cancelled')),
    price REAL NOT NULL CHECK (price >= 0),
    CHECK(length(appointment_time) = 16)
);
CREATE TABLE IF NOT EXISTS doctor_departments (
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    department_id INTEGER NOT NULL REFERENCES departments(id),
    PRIMARY KEY(doctor_id, department_id)
);
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    photo TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_time ON appointments(doctor_id, appointment_time);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_doctors_specialty ON doctors(specialty);

CREATE UNIQUE INDEX IF NOT EXISTS idx_active_doctor_slot ON appointments(doctor_id, appointment_time) WHERE status != 'cancelled';
