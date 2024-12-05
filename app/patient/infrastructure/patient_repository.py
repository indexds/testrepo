from patient.domain.patient import Patient
from patient.infrastructure.patient_entity import PatientEntity


class PatientRepository:
    def __init__(self):
        self.db = {}
        self.next_patient_id = 1

    def add_patient(self, patient: Patient) -> PatientEntity:
        # Generate a unique patient ID
        patient_id = self.next_patient_id
        self.next_patient_id += 1

        # Create a PatientEntity with ID
        patient_entity = PatientEntity(
            id=patient_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            social_security_number=patient.social_security_number
        )

        # Store the patient entity in the database
        self.db[patient_id] = patient_entity

        # Return the created patient entity
        return patient_entity

    def get_patient(self, patient_id):
        return self.db.get(patient_id)
    
    def get_all_patients(self):
        return self.db

    def get_patient_by_ss(self, patient_id, social_security_number):
        return self.db.get(social_security_number)

    def update_patient(self, patient_id,patient: Patient) -> PatientEntity :
        patient_entity = PatientEntity(
            id=patient_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            social_security_number=patient.social_security_number
        )
        return patient_entity

    def delete_patient(self, patient_id):
        return self.db.pop(patient_id)
