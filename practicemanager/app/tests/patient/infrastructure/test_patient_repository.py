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

        self.assertEqual(
            self.repository.get_patient(new_patient.id),
            PatientEntity(**{'id': new_patient.id, **patient_data})
        )

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

        self.assertEqual(
            retrieved_patient,
            PatientEntity(**{'id': new_patient.id, **patient_data})
        )

    def test_update_patient(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient = Patient(**patient_data)
        new_patient = self.repository.add_patient(patient)

        updated_data = {'first_name': 'Jane'}
        updated_patient = self.repository.update_patient(new_patient.id, updated_data)

        self.assertEqual(updated_patient.first_name, 'Jane')
        self.assertEqual(updated_patient.last_name, 'Doe')  # Ensure other fields are unchanged

    def test_delete_patient(self):
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient = Patient(**patient_data)
        new_patient = self.repository.add_patient(patient)

        self.repository.delete_patient(new_patient.id)
        self.assertIsNone(self.repository.get_patient(new_patient.id))

    def test_search_by_criteria(self):
        patient1_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient2_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1990-01-01',
            'social_security_number': '234567890123456'
        }

        self.repository.add_patient(Patient(**patient1_data))
        self.repository.add_patient(Patient(**patient2_data))

        results = self.repository.search_by_criteria({'first_name': 'Jane'})

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, 'Jane')

    def test_get_all_patients(self):
        patient1_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'social_security_number': '123456789012345'
        }
        patient2_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1990-01-01',
            'social_security_number': '234567890123456'
        }

        self.repository.add_patient(Patient(**patient1_data))
        self.repository.add_patient(Patient(**patient2_data))

        all_patients = self.repository.get_all_patients()

        self.assertEqual(len(all_patients), 2)
        self.assertEqual(all_patients[0].first_name, 'John')
        self.assertEqual(all_patients[1].first_name, 'Jane')

    def test_get_all_patients_with_pagination(self):
        for i in range(1, 21):  # Add 20 patients
            self.repository.add_patient(Patient(
                first_name=f'FirstName{i}',
                last_name=f'LastName{i}',
                date_of_birth=f'199{i}-01-01',
                social_security_number=f'{123456789012340 + i}'
            ))

        page, page_size = 2, 5
        paginated_patients, total_count = self.repository.get_all_patients_with_pagination(page, page_size)

        self.assertEqual(len(paginated_patients), 5)  # Ensure correct number of patients per page
        self.assertEqual(total_count, 20)  # Ensure total count matches
        self.assertEqual(paginated_patients[0].first_name, 'FirstName6')  # Check the first patient on page 2


if __name__ == '__main__':
    unittest.main()
