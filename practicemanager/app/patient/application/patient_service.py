from datetime import datetime

from patient.domain.patient import Patient
from patient.infrastructure.patient_entity import PatientEntity


class PatientService:
    def __init__(self, patient_repository):
        self.patient_repository = patient_repository

    def create_patient(self, patient: Patient) -> PatientEntity:
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'social_security_number']

        if any(not getattr(patient, field, None) for field in required_fields):
            raise ValueError('Patient first name is required')

        if patient.date_of_birth != datetime.strptime(patient.date_of_birth, '%Y-%m-%d') \
                .strftime('%Y-%m-%d'):
            raise ValueError('Patient date of birth is invalid')

        created_patient = self.patient_repository.add_patient(patient)
        return created_patient

    def update_patient(self, patient_id: int, updated_data: dict) -> PatientEntity:
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError('Patient not found')

        for key, value in updated_data.items():
            if hasattr(patient, key):
                setattr(patient, key, value)

        updated_patient = self.patient_repository.update_patient(patient)
        return updated_patient

    def delete_patient(self, patient_id: int) -> bool:
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError('Patient not found')

        return self.patient_repository.delete_patient(patient_id)

    def get_patient_by_id(self, patient_id: int) -> PatientEntity:
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError('Patient not found')

        return patient

    def search_patients_by_criteria(self, criteria: dict) -> list[PatientEntity]:
        patients = self.patient_repository.search_by_criteria(criteria)
        if not patients:
            raise ValueError('No patients found matching the criteria')

        return patients

    def list_all_patients(self) -> list[PatientEntity]:
        patients = self.patient_repository.get_all_patients()
        if not patients:
            raise ValueError('No patients found')

        return patients

    def list_all_patients_with_pagination(self, page: int, page_size: int) -> dict:
        if page < 1 or page_size < 1:
            raise ValueError('Page and page size must be greater than zero')

        patients, total_count = self.patient_repository.get_all_patients_with_pagination(page, page_size)
        return {
            'patients': patients,
            'total_count': total_count,
            'current_page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        }
