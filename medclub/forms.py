from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField,FileRequired,FileStorage
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from medclub.models import User,Ngo

# def choices():
#     ngoNames = Ngo.query.filter_by(is_verified=True).filter_by(blocked=False).with_entities(Ngo.id, Ngo.ngo_name)
#     final_choices = []
#     for i in ngoNames:
#         final_choices.append(i)
#     print(final_choices)
#     return final_choices


class UserRegistrationForm(FlaskForm):
    fname=StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    lname=StringField('Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    mobile=StringField('Mobile',validators=[DataRequired(),Length(min=10,max=10)])
    address=TextAreaField('Address',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=50,)])
    confirm_password=PasswordField('Confirm_pass',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    def validate_mobile(self, mobile):
        user = User.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError('Mobile Number already exist')
        try:
            if int(mobile.data):
                pass
        except ValueError:
            raise ValidationError('Only number allowed in this field')

    def validate_email(self, email):
        email_id = User.query.filter_by(email=email.data).first()
        if email_id:
            raise ValidationError('This email id is already in use')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=50,)])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class NgoRegistrationForm(FlaskForm):
    ngo_name=StringField('NGO Name',validators=[DataRequired(),Length(min=3,max=20)])
    owner_name=StringField('Owner Name',validators=[DataRequired(),Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    mobile=StringField('Mobile',validators=[DataRequired(),Length(min=10,max=10)])
    address=TextAreaField('Address',validators=[DataRequired()])
    document = FileField('Upload Document Picture',validators=[FileAllowed(['png','jpg','jpeg'])])
    password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=50,)])
    confirm_password=PasswordField('Confirm_pass',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_mobile(self, mobile):
        user = Ngo.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError('Mobile Number already exist')
        try:
            if int(mobile.data):
                pass
        except ValueError:
            raise ValidationError('Only number allowed in this field')

    def validate_email(self, email):
        email_id = Ngo.query.filter_by(email=email.data).first()
        if email_id:
            raise ValidationError('This email id is already in use')

class RequestForm(FlaskForm):
    medicine_name = StringField('Medicine Name', validators=[DataRequired(), Length(min=3, max=20)])
    quantity = StringField('Medicine Quantity', validators=[DataRequired(), Length(min=1, max=3)])
    doctor_name=StringField('Doctor Name', validators=[DataRequired(), Length(min=3, max=20)])
    prescription = FileField('Upload Prescription', validators=[FileAllowed(['png', 'jpg', 'jpeg']),DataRequired()])
    warning=BooleanField('I am accepting all ',validators=[DataRequired()])
    submit = SubmitField('Request')

    def validate_quantity(self, quantity):
        try:
            if int(quantity.data):
                pass
        except ValueError:
            raise ValidationError('Only number allowed in this field')

class DonateForm(FlaskForm):
    ngoNames = Ngo.query.filter_by(is_verified=True).filter_by(blocked=False).with_entities(Ngo.id, Ngo.ngo_name)
    final_choices = []
    for i in ngoNames:
        final_choices.append(i)
    print(final_choices)
    medicine_name = StringField('Medicine Name', validators=[DataRequired(), Length(min=3, max=20)])
    quantity = StringField('Medicine Quantity', validators=[DataRequired(), Length(min=1, max=3)])
    ngo=SelectField('Select Ngo',choices=final_choices,validators=[DataRequired()])
    expiry_date=StringField('Expiry Date', validators=[DataRequired()])
    medicine_img = FileField('Upload Medicine Image ', validators=[FileAllowed(['png', 'jpg', 'jpeg']),DataRequired()])
    warning=BooleanField('I am accepting all ',validators=[DataRequired()])
    submit = SubmitField('Donate')

    def validate_quantity(self, quantity):
        try:
            if int(quantity.data):
                pass
        except ValueError:
            raise ValidationError('Only number allowed in this field')

class RejectedForm(FlaskForm):
    comment=TextAreaField('Comment',validators=[DataRequired(),Length(min=5,max=150)])
    submit=SubmitField('Reject')

class RefillRequestForm(FlaskForm):
    medicine_name = StringField('Medicine Name', validators=[DataRequired(), Length(min=3, max=20)])
    quantity = StringField('Medicine Quantity', validators=[DataRequired(), Length(min=1, max=3)])
    doctor_name = StringField('Doctor Name', validators=[DataRequired(), Length(min=3, max=20)])
    prescription = FileField('Upload Prescription', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Resend Request')

class RefillDonationForm(FlaskForm):
    ngoNames = Ngo.query.filter_by(is_verified=True).filter_by(blocked=False).with_entities(Ngo.id, Ngo.ngo_name)
    final_choices = []
    for i in ngoNames:
        final_choices.append(i)

    medicine_name = StringField('Medicine Name', validators=[DataRequired(), Length(min=3, max=20)])
    quantity = StringField('Medicine Quantity', validators=[DataRequired(), Length(min=1, max=3)])
    ngo = SelectField('Select Ngo', choices=final_choices, validators=[DataRequired()])
    medicine_img = FileField('Upload Medicine Image ', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Re-Send Donation Request')