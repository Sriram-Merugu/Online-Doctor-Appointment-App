# urlshort.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ehr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'


db = SQLAlchemy(app)

class Patient(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))

class MedicalHistory(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    condition = db.Column(db.String(100))
    diagnosed = db.Column(db.String(20))
    notes = db.Column(db.String(255))

class Medication(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(20))
    instructions = db.Column(db.String(255))

class Allergy(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    allergen = db.Column(db.String(100))
    reaction = db.Column(db.String(255))
    severity = db.Column(db.String(50))

class Immunization(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    vaccine = db.Column(db.String(100))
    date_administered = db.Column(db.String(20))
    notes = db.Column(db.String(255))

class LabResult(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(255))
    reference_range = db.Column(db.String(255))
    date = db.Column(db.String(20))

class ClinicalNote(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.String(20))
    provider = db.Column(db.String(100))
    chief_complaint = db.Column(db.String(255))
    assessment = db.Column(db.String(255))
    plan = db.Column(db.String(255))


with app.app_context():
    db.create_all()

def add_sample_data():
    # Check if sample data already exists

    # Adding sample data to the tables
    patient = Patient(name="John Doe", dob="1980-01-01")
    db.session.add(patient)

    history1 = MedicalHistory(patient_id=patient.id, condition="Asthma", diagnosed="2010-01-01", notes="Controlled with inhalers")
    db.session.add(history1)

    history2 = MedicalHistory(patient_id=patient.id, condition="Hypertension", diagnosed="2018-05-15", notes="Controlled with medication")
    db.session.add(history2)

    medication1 = Medication(patient_id=patient.id, name="Lisinopril", dosage="10 mg", instructions="Once daily")
    db.session.add(medication1)

    medication2 = Medication(patient_id=patient.id, name="Albuterol Inhaler", dosage="90 mcg/actuation", instructions="As needed for asthma symptoms")
    db.session.add(medication2)

    allergy = Allergy(patient_id=patient.id, allergen="Penicillin", reaction="Rash, difficulty breathing", severity="Severe")
    db.session.add(allergy)

    immunization1 = Immunization(patient_id=patient.id, vaccine="Influenza", date_administered="10/15/2022", notes="Annual flu shot")
    db.session.add(immunization1)

    immunization2 = Immunization(patient_id=patient.id, vaccine="Tdap", date_administered="06/01/2020", notes="Tetanus, diphtheria, and pertussis booster")
    db.session.add(immunization2)

    lab_result1 = LabResult(patient_id=patient.id, test_name="CBC", result="Within normal limits", reference_range="-", date="02/15/2023")
    db.session.add(lab_result1)

    lab_result2 = LabResult(patient_id=patient.id, test_name="Lipid Panel", result="Total Cholesterol: 210 mg/dL, LDL: 130 mg/dL, HDL: 45 mg/dL, Triglycerides: 150 mg/dL",
                            reference_range="Total Cholesterol: < 200 mg/dL, LDL: < 100 mg/dL, HDL: > 40 mg/dL, Triglycerides: < 150 mg/dL", date="02/15/2023")
    db.session.add(lab_result2)

    clinical_note = ClinicalNote(patient_id=patient.id, date="02/15/2023", provider="Dr. Jane Smith", chief_complaint="Follow-up visit for asthma and hypertension",
                                  assessment="Asthma well-controlled with current medication. Hypertension slightly elevated, consider increasing lisinopril dosage.",
                                  plan="Increase lisinopril to 20 mg daily. Follow up in 3 months.")
    db.session.add(clinical_note)

    db.session.commit()

@app.route('/sdf')
def index():
    add_sample_data()
    patient = Patient.query.first()
    medical_history = MedicalHistory.query.filter_by(patient_id=patient.id).all()
    medications = Medication.query.filter_by(patient_id=patient.id).all()
    allergies = Allergy.query.filter_by(patient_id=patient.id).all()
    immunizations = Immunization.query.filter_by(patient_id=patient.id).all()
    lab_results = LabResult.query.filter_by(patient_id=patient.id).all()
    clinical_notes = ClinicalNote.query.filter_by(patient_id=patient.id).all()

    return render_template('index.html', patient=patient, medical_history=medical_history, medications=medications,
                           allergies=allergies, immunizations=immunizations, lab_results=lab_results,
                           clinical_notes=clinical_notes)


if __name__ == '__main__':
    
    app.run(debug=True)
    add_sample_data()  # Call the function to add sample data

