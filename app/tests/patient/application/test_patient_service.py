import unittest
import unittest.mock as mock
from patient.application.patient_service import PatientService
from patient.domain.patient import Patient


class TestPatientService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = mock.Mock()
        self.patient_service = PatientService(self.mock_repository)

    def test_create_patient(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': 123456789012345
        }

        self.mock_repository.add_patient.return_value = {'id': 1, **patient_data}

        new_patient = self.patient_service.create_patient(Patient(**patient_data))

        self.assertIsNotNone(new_patient)
        self.assertEqual(new_patient['id'], 1)
        self.assertEqual(new_patient['first_name'], 'John')
        self.assertEqual(new_patient['last_name'], 'Doe')
        self.assertEqual(new_patient['date_of_birth'], '1980-01-01')
        self.assertEqual(new_patient['social_security_number'], 123456789012345)

        self.mock_repository.add_patient.assert_called_once()

    def create_patient_with_missing_value_raises_value_error(self, missing_field):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }

        del patient_data[missing_field]

        with self.assertRaises(ValueError):
            self.patient_service.create_patient(patient_data)

    def test_create_patient_with_missing_first_name(self):
        self.create_patient_with_missing_value_raises_value_error('first_name')

    def test_create_patient_with_missing_last_name(self):
        self.create_patient_with_missing_value_raises_value_error('last_name')

    def test_create_patient_with_missing_date_of_birth(self):
        self.create_patient_with_missing_value_raises_value_error('date_of_birth')

    def test_create_patient_with_missing_social_security_number(self):
        self.create_patient_with_missing_value_raises_value_error('social_security_number')

    def test_create_patient_with_invalid_birth_date(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-13-01',
            'social_security_number': '123456789012345'
        }

        with self.assertRaises(ValueError):
            self.patient_service.create_patient(patient_data)

        self.mock_repository.add_patient.assert_not_called()


if __name__ == '__main__':
    unittest.main()
