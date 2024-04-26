from flask import Flask, render_template, send_from_directory
from flask_restful import Api
from .config import Config
import os
from flask_cors import CORS
from .database import db, migrate
from .resources import DoctorResource, PatientResource, CitaResource, TipoCitaResource, SpecialtyResource


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    api = Api(app)
    

    api.add_resource(DoctorResource, '/doctors', '/doctors/<int:id>')
    api.add_resource(SpecialtyResource, '/especialidad', '/especialidad/<int:id>')
    api.add_resource(PatientResource, '/patients', '/patients/<int:id>')
    api.add_resource(CitaResource, '/citas', '/citas/<int:id>')
    api.add_resource(TipoCitaResource, '/tipos_cita', '/tipos_cita/<int:id>')

    # Ruta para servir el frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')


    return app
