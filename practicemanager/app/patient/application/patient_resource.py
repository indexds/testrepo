from flask_restx import Namespace, Resource, fields
from flask import request, current_app as app
from patient.domain.patient import Patient

# Create Namespace
api = Namespace('patients', description='Patient management operations')

# Define patient input model for Swagger
patient_model = api.model('Patient', {
    'first_name': fields.String(required=True, description='First name of the patient'),
    'last_name': fields.String(required=True, description='Last name of the patient'),
    'date_of_birth': fields.String(required=True, description='Date of birth of the patient (YYYY-MM-DD)'),
    'social_security_number': fields.String(required=True, description='Social security number of the patient')
})

# Define response model
patient_response_model = api.model('PatientResponse', {
    'id': fields.Integer(description='Patient ID'),
    'first_name': fields.String(description='First name of the patient'),
    'last_name': fields.String(description='Last name of the patient'),
    'date_of_birth': fields.String(description='Date of birth of the patient (YYYY-MM-DD)'),
    'social_security_number': fields.String(description='Social security number of the patient')
})


@api.route('/')
class PatientList(Resource):
    @api.doc('list_all_patients')
    @api.marshal_with(patient_response_model, as_list=True)
    def get(self):
        """List all patients"""
        try:
            patient_service = app.config['patient_service']
            patients = patient_service.list_all_patients()
            return [patient.to_dict() for patient in patients], 200
        except Exception as e:
            api.abort(400, str(e))

    @api.expect(patient_model)
    @api.doc('create_patient')
    @api.marshal_with(patient_response_model, code=201)
    def post(self):
        """Create a new patient"""
        try:
            patient_data = request.get_json()
            patient_service = app.config['patient_service']
            created_patient = patient_service.create_patient(Patient(**patient_data))
            return created_patient.to_dict(), 201
        except Exception as e:
            api.abort(400, str(e))


@api.route('/<int:patient_id>')
@api.param('patient_id', 'The patient identifier')
class Patient(Resource):
    @api.doc('get_patient_by_id')
    @api.marshal_with(patient_response_model)
    def get(self, patient_id):
        """Get a patient by ID"""
        try:
            patient_service = app.config['patient_service']
            patient = patient_service.get_patient_by_id(patient_id)
            return patient.to_dict(), 200
        except Exception as e:
            api.abort(404, str(e))

    @api.expect(patient_model)
    @api.doc('update_patient')
    @api.marshal_with(patient_response_model)
    def put(self, patient_id):
        """Update a patient"""
        try:
            updated_data = request.get_json()
            patient_service = app.config['patient_service']
            updated_patient = patient_service.update_patient(patient_id, updated_data)
            return updated_patient.to_dict(), 200
        except Exception as e:
            api.abort(400, str(e))

    @api.doc('delete_patient')
    def delete(self, patient_id):
        """Delete a patient"""
        try:
            patient_service = app.config['patient_service']
            patient_service.delete_patient(patient_id)
            return {'message': 'Patient deleted successfully'}, 200
        except Exception as e:
            api.abort(400, str(e))


@api.route('/search')
class PatientSearch(Resource):
    @api.doc('search_patients')
    def get(self):
        """Search patients by criteria"""
        try:
            criteria = request.args.to_dict()
            patient_service = app.config['patient_service']
            patients = patient_service.search_patients_by_criteria(criteria)
            return [patient.to_dict() for patient in patients], 200
        except Exception as e:
            api.abort(400, str(e))


@api.route('/paginated')
class PatientListPaginated(Resource):
    @api.doc('list_all_patients_with_pagination')
    def get(self):
        """List all patients with pagination"""
        try:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))
            patient_service = app.config['patient_service']
            pagination_result = patient_service.list_all_patients_with_pagination(page, page_size)
            return {
                'patients': [patient.to_dict() for patient in pagination_result['patients']],
                'total_count': pagination_result['total_count'],
                'current_page': pagination_result['current_page'],
                'page_size': pagination_result['page_size'],
                'total_pages': pagination_result['total_pages']
            }, 200
        except Exception as e:
            api.abort(400, str(e))
