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
            'social_security_number': '123456789012345'
        }

        self.mock_repository.add_patient.return_value = mock.Mock(id=1, **patient_data)

        new_patient = self.patient_service.create_patient(Patient(**patient_data))

        self.assertIsNotNone(new_patient)
        self.assertEqual(new_patient.id, 1)
        self.assertEqual(new_patient.first_name, 'John')
        self.assertEqual(new_patient.last_name, 'Doe')
        self.assertEqual(new_patient.date_of_birth, '1980-01-01')
        self.assertEqual(new_patient.social_security_number, '123456789012345')

        self.mock_repository.add_patient.assert_called_once()

    def create_patient_with_missing_value_raises_value_error(self, missing_field):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }

        del patient_data[missing_field]

        # Passez le dictionnaire directement sans instancier `Patient`
        with self.assertRaises(ValueError):
            self.patient_service.create_patient(Patient(
                first_name=patient_data.get('first_name'),
                last_name=patient_data.get('last_name'),
                date_of_birth=patient_data.get('date_of_birth'),
                social_security_number=patient_data.get('social_security_number')
            ))

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
            self.patient_service.create_patient(Patient(**patient_data))

        self.mock_repository.add_patient.assert_not_called()

    def test_update_patient(self):
        patient_id = 1
        existing_patient = mock.Mock(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                                     social_security_number='123456789012345')
        updated_data = {'first_name': 'Jane'}

        self.mock_repository.get_patient_by_id.return_value = existing_patient
        self.mock_repository.update_patient.return_value = existing_patient

        updated_patient = self.patient_service.update_patient(patient_id, updated_data)

        self.assertIsNotNone(updated_patient)
        self.assertEqual(updated_patient.first_name, 'Jane')
        self.mock_repository.get_patient_by_id.assert_called_once_with(patient_id)
        self.mock_repository.update_patient.assert_called_once()

    def test_delete_patient(self):
        patient_id = 1
        self.mock_repository.get_patient_by_id.return_value = mock.Mock()

        result = self.patient_service.delete_patient(patient_id)

        self.assertTrue(result)
        self.mock_repository.get_patient_by_id.assert_called_once_with(patient_id)
        self.mock_repository.delete_patient.assert_called_once_with(patient_id)

    def test_delete_non_existent_patient_raises_error(self):
        patient_id = 1
        self.mock_repository.get_patient_by_id.return_value = None

        with self.assertRaises(ValueError):
            self.patient_service.delete_patient(patient_id)

        self.mock_repository.delete_patient.assert_not_called()

    def test_get_patient_by_id(self):
        patient_id = 1
        existing_patient = mock.Mock(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                                     social_security_number='123456789012345')

        self.mock_repository.get_patient_by_id.return_value = existing_patient

        patient = self.patient_service.get_patient_by_id(patient_id)

        self.assertIsNotNone(patient)
        self.assertEqual(patient.id, 1)
        self.mock_repository.get_patient_by_id.assert_called_once_with(patient_id)

    def test_get_patient_by_id_non_existent(self):
        patient_id = 1
        self.mock_repository.get_patient_by_id.return_value = None

        with self.assertRaises(ValueError):
            self.patient_service.get_patient_by_id(patient_id)

        self.mock_repository.get_patient_by_id.assert_called_once_with(patient_id)

    def test_search_patients_by_criteria(self):
        criteria = {'first_name': 'John'}
        matching_patient = mock.Mock(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                                      social_security_number='123456789012345')

        self.mock_repository.search_by_criteria.return_value = [matching_patient]

        patients = self.patient_service.search_patients_by_criteria(criteria)

        self.assertEqual(len(patients), 1)
        self.assertEqual(patients[0].first_name, 'John')
        self.mock_repository.search_by_criteria.assert_called_once_with(criteria)

    def test_search_patients_by_criteria_no_results(self):
        criteria = {'first_name': 'NonExistent'}

        self.mock_repository.search_by_criteria.return_value = []

        with self.assertRaises(ValueError):
            self.patient_service.search_patients_by_criteria(criteria)

        self.mock_repository.search_by_criteria.assert_called_once_with(criteria)

    def test_list_all_patients(self):
        patients = [
            mock.Mock(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                      social_security_number='123456789012345'),
            mock.Mock(id=2, first_name='Jane', last_name='Doe', date_of_birth='1990-01-01',
                      social_security_number='234567890123456')
        ]

        self.mock_repository.get_all_patients.return_value = patients

        result = self.patient_service.list_all_patients()

        self.assertEqual(len(result), 2)
        self.mock_repository.get_all_patients.assert_called_once()

    def test_list_all_patients_with_pagination(self):
        patients = [
            mock.Mock(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                      social_security_number='123456789012345')
        ]

        self.mock_repository.get_all_patients_with_pagination.return_value = (patients, 1)

        result = self.patient_service.list_all_patients_with_pagination(1, 10)

        self.assertEqual(result['total_count'], 1)
        self.assertEqual(len(result['patients']), 1)
        self.assertEqual(result['current_page'], 1)
        self.assertEqual(result['page_size'], 10)
        self.mock_repository.get_all_patients_with_pagination.assert_called_once_with(1, 10)


if __name__ == '__main__':
    unittest.main()
