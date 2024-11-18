from flask import Flask, request, jsonify
from flask_oidc import OpenIDConnect
from flask_restx import Api, Resource

from patient.application.patient_resource import api as patient_namespace
from patient.application.patient_service import PatientService
from patient.infrastructure.patient_repository import PatientRepository

import os

def create_app():
    app = Flask(__name__)

    # Flask-OIDC configuration
    app.config.update({
        'SECRET_KEY': 'SomethingNotEntirelySecret',
        'TESTING': True,
        'DEBUG': True,
        'OIDC_CLIENT_SECRETS': os.path.join(dirname(__file__), 'client_secrets.json'),
        'OIDC_ID_TOKEN_COOKIE_SECURE': False,
        'OIDC_USER_INFO_ENABLED': True,
        'OIDC_OPENID_REALM': 'practiceManager',
        'OIDC_SCOPES': ['openid', 'email', 'profile'],
        'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    })
    oidc = OpenIDConnect(app)

    # Initialize Flask-RESTx API
    api = Api(
        app,
        version="1.0",
        title="Patient Management API",
        description="API documentation for managing patients",
        doc="/swagger"  # Swagger UI served at /swagger
    )

    # Register the Patient namespace
    api.add_namespace(patient_namespace, path="/patients")

    # Patient configuration
    patient_repository = PatientRepository()
    patient_service = PatientService(patient_repository)
    app.config['patient_service'] = patient_service

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
