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
            'social_security_number': '123456789012345'
        }

        self.mock_service.create_patient.return_value = PatientEntity(id=1, **patient_data)

        response = self.client.post('/patients/', json=patient_data)  # Add trailing slash

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json, {'id': 1, **patient_data})
        self.mock_service.create_patient.assert_called_once()

    def test_get_patient_by_id_endpoint(self):
        patient_id = 1
        patient_data = {
            'id': patient_id,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }

        self.mock_service.get_patient_by_id.return_value = PatientEntity(**patient_data)

        response = self.client.get(f'/patients/{patient_id}')

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, patient_data)
        self.mock_service.get_patient_by_id.assert_called_once_with(patient_id)

    def test_update_patient_endpoint(self):
        patient_id = 1
        updated_data = {'first_name': 'Jane'}
        updated_patient_data = {
            'id': patient_id,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }

        self.mock_service.update_patient.return_value = PatientEntity(**updated_patient_data)

        response = self.client.put(f'/patients/{patient_id}', json=updated_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, updated_patient_data)
        self.mock_service.update_patient.assert_called_once_with(patient_id, updated_data)

    def test_delete_patient_endpoint(self):
        patient_id = 1

        self.mock_service.delete_patient.return_value = True

        response = self.client.delete(f'/patients/{patient_id}')

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, {'message': 'Patient deleted successfully'})
        self.mock_service.delete_patient.assert_called_once_with(patient_id)

    def test_search_patients_endpoint(self):
        search_criteria = {'first_name': 'John'}
        matching_patients = [
            PatientEntity(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                          social_security_number='123456789012345')
        ]

        self.mock_service.search_patients_by_criteria.return_value = matching_patients

        response = self.client.get('/patients/search', query_string=search_criteria)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, [patient.to_dict() for patient in matching_patients])
        self.mock_service.search_patients_by_criteria.assert_called_once_with(search_criteria)

    def test_list_all_patients_endpoint(self):
        patients = [
            PatientEntity(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                          social_security_number='123456789012345'),
            PatientEntity(id=2, first_name='Jane', last_name='Doe', date_of_birth='1990-01-01',
                          social_security_number='234567890123456')
        ]

        self.mock_service.list_all_patients.return_value = patients

        response = self.client.get('/patients/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, [patient.to_dict() for patient in patients])
        self.mock_service.list_all_patients.assert_called_once()

    def test_list_patients_with_pagination_endpoint(self):
        page = 1
        page_size = 10
        paginated_patients = [
            PatientEntity(id=1, first_name='John', last_name='Doe', date_of_birth='1980-01-01',
                          social_security_number='123456789012345')
        ]
        pagination_result = {
            'patients': paginated_patients,
            'total_count': 1,
            'current_page': page,
            'page_size': page_size,
            'total_pages': 1
        }

        self.mock_service.list_all_patients_with_pagination.return_value = pagination_result

        response = self.client.get('/patients/paginated', query_string={'page': page, 'page_size': page_size})

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, {
            'patients': [patient.to_dict() for patient in paginated_patients],
            'total_count': 1,
            'current_page': page,
            'page_size': page_size,
            'total_pages': 1
        })
        self.mock_service.list_all_patients_with_pagination.assert_called_once_with(page, page_size)


if __name__ == '__main__':
    unittest.main()
