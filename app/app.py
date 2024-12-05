from flask import Flask, g, request, jsonify
from flask_oidc import OpenIDConnect
from jose import JWT

from patient.application.patient_resource import patient_bp
from patient.application.patient_service import PatientService
from patient.infrastructure.patient_repository import PatientRepository
import json


def create_app():
    app = Flask(__name__)

    app.config.update({
        'SECRET_KEY': 'SomethingNotEntirelySecret',
        'TESTING': True,
        'DEBUG': True,
        'OIDC_CLIENT_SECRETS': 'client_secrets.json',
        'OIDC_ID_TOKEN_COOKIE_SECURE': False,
        'OIDC_USER_INFO_ENABLED': True,
        'OIDC_OPENID_REALM': 'practiceManager',
        'OIDC_SCOPES': ['openid', 'email', 'profile'],
        'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    })
    oidc = OpenIDConnect(app)

    @app.route('/')
    def hello_world():
        if oidc.user_loggedin:
            return ('Hello, %s, <a href="/private">See private</a> '
                    '<a href="/logout">Log out</a>') % \
                oidc.user_getfield('preferred_username')
        else:
            return 'Welcome anonymous, <a href="/private">Log in</a>'

    @app.route('/private', methods=['GET'])
    @oidc.require_login
    def private():
        user_info = oidc.user_getinfo(['email', 'preferred_username', 'sub'])
        return jsonify({
            'message': 'Welcome to the private route!',
            'user_info': user_info
        })

    @app.route('/logout')
    def logout():
        oidc.logout()
        return 'Logged out, <a href="/">Home</a>'


    @app.route('/validate', methods=['POST'])
    def validate_token():
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            keycloak_public_key = oidc.key_set[0]  # Key from Keycloak
            claims = jwt.decode(token, keycloak_public_key, algorithms=['RS256'], audience='patient-backend')
            return jsonify({'claims': claims})
        except Exception as e:
            return jsonify({'error': str(e)}), 401


    # Configuration settings, routes, middleware, etc. can be added here
    patient_repository = PatientRepository()
    patient_service = PatientService(patient_repository)
    app.config['patient_service'] = patient_service

    app.register_blueprint(patient_bp(oidc))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
