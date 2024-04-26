from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from .models import Doctor, Patient, Cita, TipoCita, Specialty, db
from .schemas import DoctorSchema, PatientSchema, CitaSchema, TipoCitaSchema, SpecialtySchema

class DoctorResource(Resource):
    def get(self, id=None):
        if id is not None:
            doctor = Doctor.query.get_or_404(id)
            schema = DoctorSchema(many=True)  
            doctor_data = schema.dump(doctor)
            appointments = Cita.query.filter_by(doctor_id=doctor.id).all()
            appointments_data = [{
                'appointment_id': appt.id,
                'appointment_date': appt.appointment_date,
                'patient_name': appt.patient.name
            } for appt in appointments]
            doctor_data['appointments_count'] = len(appointments)
            doctor_data['patients'] = appointments_data
            return doctor_data, 200
        else:
            doctors = Doctor.query.all()
            schema = DoctorSchema(many=True)  # Para múltiples doctores
            doctors_data = schema.dump(doctors)
            result = []
            for doctor_data in doctors_data:
                doctor = Doctor.query.get(doctor_data['id'])
                appointments = Cita.query.filter_by(doctor_id=doctor.id).all()
                appointments_data = [{
                    'appointment_id': appt.id,
                    'appointment_date': appt.appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'patient_name': appt.patient.name if appt.patient else None
                } for appt in appointments]
                doctor_data['appointments_count'] = len(appointments)
                doctor_data['patients'] = appointments_data
                result.append(doctor_data)
            return result, 200
        

    def post(self):
        schema = DoctorSchema()
        try:
            doctor_data = request.get_json()
            doctor = schema.load(doctor_data, session=db.session)
            db.session.add(doctor)
            db.session.commit()
            return schema.dump(doctor), 201
        except ValidationError as err:
            # Aquí puedes devolver un mensaje de error más descriptivo
            return {'message': 'Error de validación', 'errors': err.messages}, 400
    
    def put(self, id):
        schema = DoctorSchema()
        doctor = Doctor.query.get_or_404(id)
        try:
            updated_doctor = schema.load(request.get_json(), instance=doctor, session=db.session)
            db.session.commit()
            return schema.dump(updated_doctor), 200
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, id):
        doctor = Doctor.query.get_or_404(id)
        db.session.delete(doctor)
        db.session.commit()
        return '', 204
    
class PatientResource(Resource):
    def get(self, id=None):
        schema = PatientSchema(many=(id is None))
        try:
            patients = Patient.query.all() if id is None else Patient.query.get_or_404(id)
            return schema.dump(patients), 200
        except ValidationError as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    def post(self):
        schema = PatientSchema()
        try:
            patient = schema.load(request.get_json(), session=db.session)
            db.session.add(patient)
            db.session.commit()
            return schema.dump(patient), 201
        except ValidationError as err:
            db.session.rollback()
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def put(self, id):
        patient = Patient.query.get_or_404(id)
        schema = PatientSchema()
        try:
            updated_patient = schema.load(request.get_json(), instance=patient, session=db.session)
            db.session.commit()
            return schema.dump(updated_patient), 200
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, id):
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        return '', 204

class CitaResource(Resource):
    def get(self, id=None):
        schema = CitaSchema(many=(id is None))
        try:
            citas = Cita.query.all() if id is None else Cita.query.get_or_404(id)
            return schema.dump(citas), 200
        except ValidationError as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    def post(self):
        schema = CitaSchema()
        try:
            cita = schema.load(request.get_json(), session=db.session)
            db.session.add(cita)
            db.session.commit()
            return schema.dump(cita), 201
        except ValidationError as err:
            db.session.rollback()
            return {'message': 'Validation error', 'errors': err.messages}, 400
    
    def put(self, id):
        cita = Cita.query.get_or_404(id)
        schema = CitaSchema()
        try:
            updated_cita = schema.load(request.get_json(), instance=cita, session=db.session)
            db.session.commit()
            return schema.dump(updated_cita), 200
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, id):
        cita = Cita.query.get_or_404(id)
        db.session.delete(cita)
        db.session.commit()
        return '', 204

class TipoCitaResource(Resource):
    def get(self, id=None):
        schema = TipoCitaSchema(many=(id is None))
        try:
            tipos = TipoCita.query.all() if id is None else TipoCita.query.get_or_404(id)
            return schema.dump(tipos), 200
        except ValidationError as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    def post(self):
        schema = TipoCitaSchema()
        try:
            tipo = schema.load(request.get_json(), session=db.session)
            db.session.add(tipo)
            db.session.commit()
            return schema.dump(tipo), 201
        except ValidationError as err:
            db.session.rollback()
            return {'message': 'Validation error', 'errors': err.messages}, 400
    
    def put(self, id):
        tipo = TipoCita.query.get_or_404(id)
        schema = TipoCitaSchema()
        try:
            updated_tipo = schema.load(request.get_json(), instance=tipo, session=db.session)
            db.session.commit()
            return schema.dump(updated_tipo), 200
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, id):
        tipo = TipoCita.query.get_or_404(id)
        db.session.delete(tipo)
        db.session.commit()
        return '', 204

class SpecialtyResource(Resource):
    def get(self, id=None):
        schema = SpecialtySchema(many=(id is None))
        try:
            specialties = Specialty.query.all() if id is None else Specialty.query.get_or_404(id)
            return schema.dump(specialties), 200
        except ValidationError as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    def post(self):
        schema = SpecialtySchema()
        specialty_data = request.get_json()
        try:
            specialty = schema.load(specialty_data, session=db.session)
            db.session.add(specialty)
            db.session.commit()
            return schema.dump(specialty), 201
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400

    def put(self, id):
        specialty = Specialty.query.get_or_404(id)
        schema = SpecialtySchema()
        try:
            updated_specialty = schema.load(request.get_json(), instance=specialty, session=db.session)
            db.session.commit()
            return schema.dump(updated_specialty), 200
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, id):
        specialty = Specialty.query.get_or_404(id)
        db.session.delete(specialty)
        db.session.commit()
        return '', 204
