import unittest
from unittest.mock import Mock
from flask.testing import FlaskClient

from app import create_app
from patient.application.patient_service import PatientService
from patient.infrastructure.patient_entity import PatientEntity


class TestPatientResource(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client: FlaskClient = self.app.test_client()

        self.mock_service = Mock(spec=PatientService)
        self.app.config['patient_service'] = self.mock_service

    def test_create_patient_endpoint(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': 123456789012345
        }

        self.mock_service.create_patient.return_value = PatientEntity(**{'id': 1, **patient_data})

        response = self.client.post('/patients', json=patient_data)

        self.assertEqual(201, response.status_code)
        print(response.json)
        self.assertEqual(response.json, {'id': 1, **patient_data})
        self.mock_service.create_patient.assert_called_once()
