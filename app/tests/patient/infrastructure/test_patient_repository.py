import unittest
from patient.domain.patient import Patient
from patient.infrastructure.patient_entity import PatientEntity
from patient.infrastructure.patient_repository import PatientRepository


class TestPatientRepository(unittest.TestCase):
    def setUp(self):
        self.repository = PatientRepository()

    def test_add_patient(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient = Patient(**patient_data)
        new_patient = self.repository.add_patient(patient)

        self.assertEqual(self.repository.get_patient(new_patient.id), PatientEntity(**{'id': 1, **patient_data}))

    def test_get_patient(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient = Patient(**patient_data)
        new_patient = self.repository.add_patient(patient)

        retrieved_patient = self.repository.get_patient(new_patient.id)

        self.assertEqual(retrieved_patient, PatientEntity(**{'id': 1, **patient_data}))
