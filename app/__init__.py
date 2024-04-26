from flask import Flask
from flask_restful import Api
from .config import Config
from flask_cors import CORS
from .database import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    
    api = Api(app)
    
    # Para APIRestFul
    from .resources import DoctorResource, PatientResource, CitaResource, TipoCitaResource, SpecialtyResource

    api.add_resource(DoctorResource, '/doctors', '/doctors/<int:id>')
    api.add_resource(SpecialtyResource, '/especialidad', '/especialidad/<int:id>')
    api.add_resource(PatientResource, '/patients', '/patients/<int:id>')
    api.add_resource(CitaResource, '/citas', '/citas/<int:id>')
    api.add_resource(TipoCitaResource, '/tipos_cita', '/tipos_cita/<int:id>')


    return app
