from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from .models import Cita, TipoCita, Doctor, Specialty, Patient

class SpecialtySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Specialty
        load_instance = True

    id = auto_field()
    name = auto_field()

class DoctorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor
        load_instance = True
        include_fk = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    specialty_id = auto_field()
    specialty = Nested(SpecialtySchema, only=('id', 'name'), dump_only=True) 

class PatientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True

class TipoCitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TipoCita
        load_instance = True

class CitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cita
        include_fk = True
        load_instance = True

    # Esquemas anidados para doctor y paciente
    doctor = Nested(DoctorSchema, only=('id', 'name', 'specialty'))
    patient = Nested(PatientSchema, only=('id','name', 'age'))
    tipo = Nested(TipoCitaSchema, only=('id', 'nombre'))