from . import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'),nullable=False)
    appointments = db.relationship('Cita', backref='doctor', lazy='dynamic')

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    doctors = db.relationship('Doctor', backref='specialty', lazy='dynamic')


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    appointments = db.relationship('Cita', back_populates='patient')

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_cita.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)

    patient = db.relationship('Patient', back_populates='appointments')

class TipoCita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    citas = db.relationship('Cita', backref='tipo', lazy=True)