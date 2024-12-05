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

    def get_all_patients(self):
        """Retrieve all patients."""
        return list(self.patient_repository.get_all_patients().values())

    def get_patient(self, patient_id):
        """Retrieve a single patient by ID."""
        return self.patient_repository.get_patient(patient_id)

    def update_patient(self, patient_id, patient_data):
        """Update a patient."""
        patient = Patient(**patient_data)
        updated_patient = self.patient_repository.update_patient(patient_id, patient)
        return updated_patient

    def delete_patient(self, patient_id):
        """Delete a patient."""
        return self.patient_repository.delete_patient(patient_id)
