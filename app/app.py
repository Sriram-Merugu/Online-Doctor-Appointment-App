from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TextAreaField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import smtplib
from wtforms.validators import DataRequired
from datetime import date
import random
from flask_bootstrap import Bootstrap
from wtforms import StringField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Length, InputRequired, Optional, Regexp



MY_EMAIL = "yunoastha3@gmail.com"
MY_PASSWORD = "rgnjfotowrqpenoe"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {
    'two': 'sqlite:///ehr.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create SQLAlchemy instances
bootstrap = Bootstrap(app)


class MedicalHistoryForm(FlaskForm):
    condition = StringField('Condition', validators=[DataRequired(), Length(max=100)])
    diagnosed = StringField('Diagnosed', validators=[DataRequired(), Length(max=20)])
    notes = StringField('Notes', validators=[Optional(), Length(max=500)])


class MedicationForm(FlaskForm):
    medication = StringField('Medication', validators=[DataRequired(), Length(max=100)])
    dosage = StringField('Dosage', validators=[DataRequired(), Length(max=20)])
    instructions = StringField('Instructions', validators=[DataRequired(), Length(max=200)])

class ImmunizationForm(FlaskForm):
    vaccine = StringField('Vaccine', validators=[DataRequired(), Length(max=100)])
    date_administered = StringField('Date Administered', validators=[DataRequired(), Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$', message="Invalid date format. Use MM/DD/YYYY.")])
    notes = StringField('Notes', validators=[Optional(), Length(max=200)])

class LabResultForm(FlaskForm):
    test_name = StringField('Test Name', validators=[DataRequired(), Length(max=100)])
    result = StringField('Result', validators=[DataRequired(), Length(max=200)])
    reference_range = StringField('Reference Range', validators=[Optional(), Length(max=200)])
    date = StringField('Date', validators=[DataRequired(), Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$', message="Invalid date format. Use MM/DD/YYYY.")])

class ClinicalNoteForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired(), Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$', message="Invalid date format. Use MM/DD/YYYY.")])
    provider = StringField('Provider', validators=[DataRequired(), Length(max=100)])
    chief_complaint = StringField('Chief Complaint', validators=[DataRequired(), Length(max=200)])
    assessment = TextAreaField('Assessment', validators=[DataRequired(), Length(max=500)])
    plan = TextAreaField('Plan', validators=[DataRequired(), Length(max=500)])

class AllergiesForm(FlaskForm):
    allergy = StringField('Allergy')
    reaction = StringField('Reaction')
    severity = StringField('Severity')



class EHRForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired(), Length(max=100)])
    patient_dob = StringField('Date of Birth', validators=[DataRequired(), Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$', message="Invalid date format. Use MM/DD/YYYY.")])
    current_conditions = StringField('Current Conditions', validators=[Optional(), Length(max=200)])
    allergies = StringField('Allergies', validators=[Optional(), Length(max=200)])
    recent_visits = StringField('Recent Visits', validators=[Optional(), Length(max=200)])
    medical_history = FieldList(FormField(MedicalHistoryForm), min_entries=1, validators=[InputRequired()])
    medications = FieldList(FormField(MedicationForm), min_entries=1, validators=[InputRequired()])
    add_allergies = FieldList(FormField(AllergiesForm), min_entries=1)
    immunizations = FieldList(FormField(ImmunizationForm), min_entries=1, validators=[InputRequired()])
    lab_results = FieldList(FormField(LabResultForm), min_entries=1, validators=[InputRequired()])
    clinical_notes = FieldList(FormField(ClinicalNoteForm), min_entries=1, validators=[InputRequired()])


##CREATE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    phone = db.Column(db.String(10))


class HealthRecord(db.Model):
    __tablename__ = "health_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    medical_condition = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(200))
    # Add more fields as needed


class HealthRecordForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    medical_condition = StringField('Medical Condition', validators=[DataRequired()])
    treatment = TextAreaField('Treatment')
    submit = SubmitField('Save Record')


class doctors_info(db.Model):
    __tablename__ = "doctors"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    residency = db.Column(db.String(100), nullable=False)
    fellowship = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    certified = db.Column(db.String(100), nullable=False)
    license = db.Column(db.String(100), nullable=False)
    lang = db.Column(db.String(100), nullable=False)


class webmedconsultmaster(db.Model):
    __tablename__ = "doctor_video_call_requests"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    Weight = db.Column(db.Integer, nullable=False)
    bloodgroup = db.Column(db.String(50), nullable=False)
    issue = db.Column(db.String(250), nullable=False)


class Appoinment(db.Model):
    __tablename__ = "appointments"  
    sno = db.Column(db.Integer, primary_key=True)
    appoinmentname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    doctor = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(250), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} {self.appoinmentname} {self.email} {self.doctor} {self.message}"


class Contact(db.Model):
    __tablename__ = "contacts"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(250), nullable=False)

class Patient(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))

class MedicalHistory(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'medical_history'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    condition = db.Column(db.String(100))
    diagnosed = db.Column(db.String(20))
    notes = db.Column(db.String(255))

class Medication(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(20))
    instructions = db.Column(db.String(255))

class Allergy(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'allergy'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    allergen = db.Column(db.String(100))
    reaction = db.Column(db.String(255))
    severity = db.Column(db.String(50))

class Immunization(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'immunization'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    vaccine = db.Column(db.String(100))
    date_administered = db.Column(db.String(20))
    notes = db.Column(db.String(255))

class LabResult(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'lab_result'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(255))
    reference_range = db.Column(db.String(255))
    date = db.Column(db.String(20))

class ClinicalNote(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'clinical_note'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.String(20))
    provider = db.Column(db.String(100))
    chief_complaint = db.Column(db.String(255))
    assessment = db.Column(db.String(255))
    plan = db.Column(db.String(255))





with app.app_context():
    db.create_all()


# @app.route('/')
# def hello_world():
#     # return 'Hello, World!'
#     return render_template('index.html')

year = date.today().year


@app.route('/')
def home():
    return render_template("index.html", home_page=True, year=year)


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('signin'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('signin'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('doctor'))

    return render_template("signin.html", logged_in=current_user.is_authenticated)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, sign in instead!")
            return redirect(url_for('signin'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("doctor"))

    return render_template("signin.html", logged_in=current_user.is_authenticated, signup_page=True)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


pwd = None
changing_pwd_email = None



@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        global pwd, changing_pwd_email
        if not User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You don't have an account , sign up instead!")
            return redirect(url_for('signup'))

        pwd = random.randint(1000, 9999)
        changing_pwd_email = request.form.get('email')
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=changing_pwd_email,
                                msg=f"Subject: Change your password ,\n\n Your otp is, it is valid for 1 minute {pwd}".encode(
                                    "utf8")
                                )

        return render_template("forgot_pwd.html", logged_in=current_user.is_authenticated, forgot_p=True)
    return render_template("forgot_pwd.html", logged_in=current_user.is_authenticated, forgot_e=True)


@app.route('/valid_otp', methods=["GET", "POST"])
def valid_otp():
    global pwd
    if request.method == "POST":
        otp = request.form.get("otp")
        if otp == str(pwd):
            return render_template("forgot_pwd.html",  logged_in=current_user.is_authenticated, new_pass=True)
        else:
            flash("Invalid OTP, try again")
            return redirect(url_for("signin"))

@app.route('/change_pwd', methods=["GET", "POST"])
def change_pwd():
    if request.method == "POST":
        global changing_pwd_email
        user = User.query.filter_by(email=changing_pwd_email).first()
        if user:
            # Hash and salt the new password
            hashed_password = generate_password_hash(request.form.get('password'))

            # Update the user's password attribute with the new hashed password
            user.password = hashed_password

            # Commit the changes to the database
            db.session.commit()

            flash("Password changed successfully. Please sign in with your new password.")
            return redirect(url_for('signin'))
        else:
            flash("User not found.")
            return redirect(url_for('forgot_password'))


@app.route('/doctor/profile',methods=['GET','POST'])
def profile():
    user = current_user
    id = user.id
    medical_his = MedicalHistory.query.filter_by(patient_id=id)
    medication = Medication.query.filter_by(patient_id=id)
    allergies = Allergy.query.filter_by(patient_id=id)
    immune = Immunization.query.filter_by(patient_id=id)
    lab_result = LabResult.query.filter_by(patient_id=id)
    notes = ClinicalNote.query.filter_by(patient_id=id)

    if request.method == "POST":
        if user:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')

            if phone.isnumeric() and len(phone) == 10:

                # Hash and salt the new password
                hashed_password = generate_password_hash(request.form.get('password'))
                # Update the user's password attribute with the new hashed password
                user.password = hashed_password
                user.name = name
                user.email = email
                user.phone = phone
                # Commit the changes to the database
                db.session.commit()

                flash("Profile changed successfully.")
                return redirect(url_for('profile'),)
            else:
                flash("Enter correct 10 digit numeric number")
        else:
            flash("User not found.")


    return render_template('profile.html', user=user, medical_his=medical_his, medication=medication, allergies=allergies, immune=immune, lab_result=lab_result, notes=notes)

@app.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    # return 'Hello, World!'
    if request.method == 'POST':
        # gender = request.form['gender']
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            print("OK")
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject: Email from {name} , from the web-med consultant\n\n{message}\nemail id of the consultant: {email}".encode(
                                    "utf8")
                                )

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        return render_template('return3.html')
    return redirect(url_for("doctor"))


@app.route('/form', methods=["GET", "POST"])
@login_required
def form():
    if request.method == 'POST':
        # gender = request.form['gender']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        Age = request.form['Age']
        gender = request.form['gender']
        height = request.form['height']
        Weight = request.form['Weight']
        bloodgroup = request.form['bloodgroup']
        issue = request.form['issue']

        new_request = webmedconsultmaster(name=name, phone=phone, email=email, Age=Age, gender=gender, height=height,
                                          Weight=Weight, bloodgroup=bloodgroup, issue=issue)
        db.session.add(new_request)
        db.session.commit()
        return render_template('return.html')

    # return 'Hello, World!'
    return render_template('form.html')


def send_mail(patient_name, email, hospital_name, visit_reason, medical_service, appointment_date_time):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        print("OK")
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=email,
                            msg=f'''Subject: Information regarding your appointment at {hospital_name} hospital.\n\n
                                    🔶🔷WebConsult🔷🔶 \n

Hello {patient_name},\n

Thank you for submitting your appointment to webconsult. Your appointment regarding {medical_service} service is successfull. Your appointment is scheduled for the {appointment_date_time}.
\n
Time: 3:00-4:40 PM\n
Venue: {hospital_name}\n
\n
We request you to be present at the venue 10min prior to your assigned slot\n
\n
Best Regards,\n
Team Webconsult\n
                                    '''.encode("utf8")

                            )


@app.route('/doctor')
@login_required
def doctor():
    print(current_user.name)
    return render_template("index.html", name=current_user.name, logged_in=True, year=year)


@app.route('/videocall')
@login_required
def videocall():
    # return 'Hello, World!'
    return render_template('videocall.html')


@app.route('/home/doctors/<int:sno>', methods=["GET", "POST"])
@login_required
def doctors(sno):
    # return 'Hello, World!'
    doctors_information = doctors_info.query.get(sno)
    return render_template('doctors.html', doc=doctors_information)


@app.route('/docs')
def docs():
    # return 'Hello, World!'
    return render_template('docs.html')


@app.route('/gmeet')
def gmeet():
    # return 'Hello, World!'
    return render_template('gmeet.html')


@app.route('/appointment', methods=["GET", "POST"])
def appointment():
    if request.method == 'POST':
        patient_name = request.form.get('patientName')
        dob = request.form.get('dob')
        contact_info = request.form.get('contactInfo')
        email = request.form.get('email')
        appointment_date_time = request.form.get('appointmentDateTime')
        visit_reason = request.form.get('visitReason')
        hospital_name = request.form.get('hospitalName')
        medical_service = request.form.get('medicalService')
        # Now you can use the variables above in your application
        # ...

        send_mail(patient_name, email, hospital_name, visit_reason, medical_service, appointment_date_time)

        return render_template('return2.html')
    # return 'Hello, World!'
    return render_template('appoinment.html')


# ---- function related to doctor and how to join ------


@app.route('/dashbord')
def dashbord():
    return render_template('dashbord.html', first_name='hi', last_name='hello')


@app.route('/meeting')
def meeting():
    return render_template('meeting.html', user_name=current_user.name, id=current_user.id)


@app.route("/join", methods=["GET", "POST"])
def join():
    if current_user:
        return redirect(f"/meeting?roomID={current_user.id}")




@app.route('/ehr/create', methods=['GET', 'POST'])
def create_ehr():
    form = EHRForm()
    if request.method == 'POST' :
        # Process the form data
        data = form.data
        # Save the data to the backend (e.g., database)
        # ...

        print(data)
        return redirect(url_for('home'))
    return render_template('create_ehr.html', form=form)






if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50001)
