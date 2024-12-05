class PatientEntity:
    def __init__(self, id: int, first_name: str, last_name: str, date_of_birth: str, social_security_number: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.social_security_number = social_security_number

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'social_security_number': self.social_security_number
        }

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
