from flask import request, jsonify, Blueprint
from flask import current_app as app
from patient.domain.patient import Patient
import requests
from functools import wraps


def patient_bp(oidc):
    patient_bp = Blueprint('patient', __name__)
    @patient_bp.route('/patients', methods=['POST'])
    @oidc.require_login
    def create_patient():
        """Create a new patient."""
        try:
            patient_data = request.get_json()
            patient_service = app.config['patient_service']
            created_patient = patient_service.create_patient(Patient(**patient_data))
            return jsonify(created_patient.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @patient_bp.route('/patients', methods=['GET'])
    @oidc.require_login
    def get_all_patients():
        """Retrieve all patients."""
        try:
            patient_service = app.config['patient_service']
            patients = patient_service.get_all_patients()
            return jsonify([patient.to_dict() for patient in patients]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
    @oidc.require_login
    def get_patient(patient_id):
        """Retrieve a specific patient by ID."""
        try:
            patient_service = app.config['patient_service']
            patient = patient_service.get_patient(patient_id)
            if patient:
                return jsonify(patient.to_dict()), 200
            return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
    @oidc.require_login
    def update_patient(patient_id):
        """Update a specific patient by ID."""
        try:
            patient_data = request.get_json()
            patient_service = app.config['patient_service']
            updated_patient = patient_service.update_patient(patient_id, patient_data)
            if updated_patient:
                return jsonify(updated_patient.to_dict()), 200
            return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
    @oidc.require_login
    def delete_patient(patient_id):
        """Delete a specific patient by ID."""
        try:
            patient_service = app.config['patient_service']
            success = patient_service.delete_patient(patient_id)
            if success:
                return jsonify({'message': 'Patient deleted successfully'}), 200
            return jsonify({'error': 'Patient not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return patient_bp
