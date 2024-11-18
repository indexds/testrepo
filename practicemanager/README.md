# Practice Manager

## First US and acceptance tests

As a doctor Thomas  
I want to keep records of my patients  
So that i can access them later

Acceptance criteria / Acceptance tests

Scenario: Create a patient  
Given I am a doctor Thomas  
When I create a patient John Doe with the social security number 123456789123456    
Then I should see the patient in the list of patients

Scenario: Search a patient by social security number  
Given I am a doctor Thomas   
And I have a patient John Doe with the social security number 123456789123456    
When I search for the patient with the social security number 123456789123456  
Then I should see the patient John Die in the list of patients  

Scenario: Search a patient by name  
Given I am a doctor Thomas  
And I have a patient John Doe with the social security number 123456789123456  
When I search for the patient with the name John Doe  
Then I should see the patient John Die in the list of patients  

Scenario: Search a patient by surname  
Given I am a doctor Thomas  
And I have a patient John Doe with the social security number 123456789123456  
When I search for the patient with the surname Doe  
Then I should see the patient John Die in the list of patients  

Scenario: Update a patient  
Given I am a doctor Thomas  
And I have a patient John Doe with the social security number 123456789123456  
When I update the patient John Doe with the social security number 123456789123457  
Then I should see the patient John Doe in the list of patients  
And his social security number should be 123456789123457  

Scenario: Delete a patient  
Given I am a doctor Thomas  
And I have a patient John Doe with the social security number 123456789123456  
When I delete the patient John Doe  
Then I should not see the patient John Doe in the list of patients  

Scenario: Get a patient by ID  
Given I am a doctor Thomas  
And I have a patient John Doe with the ID 1  
When I get the patient with the ID 1  
Then I should see the patient John Doe informations

## Run tests using CLI

```bash
python -m unittest tests.patient.application.test_patient_service 
```

## Launch the application

```bash
 flask run
```

## A curl example to create a patient:

```bash
curl -v -X POST -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "date_of_birth": "1980-01-01", "social_security_number": 123456789012345}' \
  http://127.0.0.1:5000/patients
```