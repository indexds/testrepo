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

    def get_patient(self, patient_id: int) -> PatientEntity:
        # Retrieve a patient by ID
        return self.db.get(patient_id)

    def update_patient(self, patient_id: int, updated_data: dict) -> PatientEntity:
        # Update a patient's information
        patient_entity = self.db.get(patient_id)
        if not patient_entity:
            raise ValueError("Patient not found")

        # Update fields dynamically
        for key, value in updated_data.items():
            if hasattr(patient_entity, key):
                setattr(patient_entity, key, value)

        # Save the updated patient back into the database
        self.db[patient_id] = patient_entity
        return patient_entity

    def delete_patient(self, patient_id: int) -> bool:
        # Delete a patient by ID
        if patient_id in self.db:
            del self.db[patient_id]
            return True
        else:
            raise ValueError("Patient not found")

    def search_by_criteria(self, criteria: dict) -> list[PatientEntity]:
        # Search patients based on criteria (e.g., first_name, last_name, etc.)
        results = []
        for patient in self.db.values():
            match = all(
                getattr(patient, key, None) == value
                for key, value in criteria.items()
            )
            if match:
                results.append(patient)
        return results

    def get_all_patients(self) -> list[PatientEntity]:
        # Retrieve all patients
        return list(self.db.values())

    def get_all_patients_with_pagination(self, page: int, page_size: int) -> tuple:
        # Implement pagination for retrieving all patients
        all_patients = list(self.db.values())
        start = (page - 1) * page_size
        end = start + page_size

        # Paginate the patient list
        paginated_patients = all_patients[start:end]
        total_count = len(all_patients)

        return paginated_patients, total_count

    def get_patient_by_id(self, patient_id: int) -> PatientEntity:
        # Retrieve a patient by ID
        patient_entity = self.db.get(patient_id)
        if not patient_entity:
            raise ValueError("Patient not found")
        return patient_entity
