from flask import render_template, url_for, flash, redirect, abort, session
from flask import request
import flask
from medclub import app, db
from medclub.forms import NgoRegistrationForm, UserRegistrationForm, LoginForm, RequestForm, DonateForm, RejectedForm, \
    RefillRequestForm, RefillDonationForm
from medclub.models import Ngo, User, Request, Donate, Report, Admin
import secrets
import os
from PIL import Image
from passlib.hash import sha256_crypt

#edit
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField,FileRequired,FileStorage
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

def choices():
    ngoNames = Ngo.query.filter_by(is_verified=True).filter_by(blocked=False).with_entities(Ngo.id, Ngo.ngo_name)
    final_choices = []
    for i in ngoNames:
        final_choices.append(i)
    print(final_choices)
    return final_choices

class DonationForm(FlaskForm):
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

def encodePass(password):
    password = sha256_crypt.hash(password)
    return password


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_name)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


def save_prescription(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/presc', picture_name)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


def save_medicine_img(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/medicine_img', picture_name)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


@app.context_processor
def inject_user():
    total_user_count = db.session.query(User).count()
    total_ngo_count = db.session.query(Ngo).count()
    return dict(user=total_user_count, ngo=total_ngo_count)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home Page')


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Page')


@app.route('/userLogin', methods=['GET', 'POST'])
def ulogin():
    if session.get('user_id'):
        return redirect(url_for('udash'))
    form = LoginForm()
    if form.validate_on_submit():
        # email_id=form.email.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and sha256_crypt.verify(form.password.data, user.password):
            if user.blocked==True:
                flash('You are blocked beacause of suspicious activity', 'danger')
                return redirect(url_for('home'))
            session['user_id'] = user.id
            type = 'user'
            return redirect(url_for('udash'))
        else:
            flash('Login Unsuccessful please check you email id or password', 'danger')
    return render_template('user_login.html', title='User Login Page', form=form)


@app.route('/ngoLogin', methods=['GET', 'POST'])
def nlogin():
    if session.get('ngo_id'):
        return redirect(url_for('ndash'))
    form = LoginForm()
    if form.validate_on_submit():
        # email_id=form.email.data
        ngo = Ngo.query.filter_by(email=form.email.data).first()
        if ngo and sha256_crypt.verify(form.password.data, ngo.password):
            if ngo.blocked==True:
                flash('You are blocked beacause of suspicious activity', 'danger')
                return redirect(url_for('home'))
            if ngo.is_verified==False:
                flash('Your account is not accepted by Admin please wait', 'danger')
                return redirect(url_for('home'))
            session['ngo_id'] = ngo.id
            return redirect(url_for('ndash'))
        else:
            flash('Login Unsuccessful please check you email id or password', 'danger')
            return redirect(url_for('nlogin'))
    return render_template('ngo_login.html', title='NGO Login Page', form=form)


@app.route('/userRegister', methods=['POST', 'GET'])
def ureg():
    if session.get('ngo_id'):
        return redirect(url_for('udash'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        password = encodePass(form.password.data)
        user = User(fname=form.fname.data, lname=form.lname.data, mobile=form.mobile.data, email=form.email.data,
                    password=password, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! Now you are able to login', 'success')
        return redirect(url_for('ulogin'))
    return render_template('user_registration.html', title='User Registration Page', form=form)


@app.route('/ngoRegister', methods=['POST', 'GET'])
def nreg():
    form = NgoRegistrationForm()
    if form.validate_on_submit():
        password = encodePass(form.password.data)
        picture_file = save_picture(form.document.data)
        ngo = Ngo(ngo_name=form.ngo_name.data, owner_name=form.owner_name.data, password=password,
                  email=form.email.data, mobile=form.mobile.data, address=form.address.data,
                  upload_verified_doc=picture_file)
        db.session.add(ngo)
        db.session.commit()
        flash(f'Your Account has been created! Now you are able to login', 'success')
        return redirect(url_for('nlogin'))
    return render_template('ngo_registration.html', title='NGO Registration Page', form=form)


@app.route('/udash', methods=['GET', 'POST'])
def udash():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        type = 'user'
        user = User.query.get_or_404(session['user_id'])
        name = str.capitalize(user.fname + ' ' + user.lname)
        total_req = Request.query.filter_by(requester_user_id=session['user_id']).count()
        total_deliver_req = Request.query.filter_by(delivered=True).filter_by(
            requester_user_id=session['user_id']).count()
        total_accepted_req = Request.query.filter_by(accepted=True).filter_by(
            requester_user_id=session['user_id']).count()
        total_pending_req = Request.query.filter_by(accepted=False).filter_by(rejected=False).filter_by(
            requester_user_id=session['user_id']).count()
        total_rejected = Request.query.filter_by(rejected=True).filter_by(requester_user_id=session['user_id']).count()
        total_don = Donate.query.filter_by(donater_user_id=session['user_id']).count()
        total_accepted_don = Donate.query.filter_by(accepted=True).filter_by(donater_user_id=session['user_id']).count()
        total_pending_don = Donate.query.filter_by(accepted=False).filter_by(rejected=False).filter_by(
            donater_user_id=session['user_id']).count()
        total_don_rejected = Donate.query.filter_by(rejected=True).filter_by(donater_user_id=session['user_id']).count()
        total_don_deliver = Donate.query.filter_by(delivered=True).filter_by(donater_user_id=session['user_id']).count()
        info = [total_don, total_accepted_don, total_pending_don, total_don_rejected, total_req, total_accepted_req,
                total_pending_req, total_rejected, total_deliver_req, total_don_deliver]
        return render_template('udash.html', title='NGO Registration Page', name=name, type=type, info=info)


@app.route('/ndash', methods=['GET', 'POST'])
def ndash():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        type = 'ngo'
        ngo = Ngo.query.get_or_404(session['ngo_id'])
        name = ngo.ngo_name
        total_request=Request.query.filter_by(donater_ngo_id=ngo.id).count()
        total_donate=Donate.query.filter_by(receiver_ngo_id=ngo.id).filter_by(accepted=True).count()
        data=[total_request,total_donate]
        return render_template('ndash.html', title='NGO Registration Page', type=type, name=name,data=data)


@app.route('/user_logout', methods=['GET', 'POST'])
def userlogout():
    if session.get('user_id'):
        session.pop('user_id', None)
        return redirect(url_for('home'))
    elif not session.get('user_id'):
        return redirect(url_for('home'))

@app.route('/ngo_logout', methods=['GET', 'POST'])
def ngologout():
    if session.get('ngo_id'):
        session.pop('ngo_id', None)
        return redirect(url_for('home'))
    elif not session.get('ngo_id'):
        return redirect(url_for('home'))


@app.route('/request', methods=['GET', 'POST'])
def request():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        user=User.query.filter_by(id=session['user_id']).first()
        if user.is_verified==False:
            flash('You are not verfied by the admin', 'danger')
            return redirect(url_for('udash'))
        form = RequestForm()
        type = 'user'
        if form.validate_on_submit():
            prescription_file = save_prescription(form.prescription.data)
            req = Request(medicine_name=form.medicine_name.data, doctor_name=form.doctor_name.data,
                          quantity=int(form.quantity.data), prescription=prescription_file,
                          requester_user_id=session['user_id'])
            db.session.add(req)
            db.session.commit()
            flash('Request for medicine is submitted sucessfully', 'success')
            return redirect(url_for('udash'))
        return render_template('Request.html', title='NGO Login Page', form=form, type=type)


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        form = DonationForm()
        type = 'user'
        if form.validate_on_submit():
            med_img = save_medicine_img(form.medicine_img.data)
            donate = Donate(medicine_name=form.medicine_name.data, donater_user_id=session['user_id'],
                            quantity=int(form.quantity.data), receiver_ngo_id=form.ngo.data, medicine_img=med_img,expiry_date=form.expiry_date.data)
            db.session.add(donate)
            db.session.commit()
            flash('Donatation Request for medicine is submitted sucessfully', 'success')
            return redirect(url_for('udash'))
        return render_template('Donate.html', title='NGO Login Page', form=form, type=type)


@app.route('/pending_request', methods=['GET', 'POST'])
def pendingRequest():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        type = 'ngo'
        requests = db.session.query(Request).filter_by(accepted=False).filter_by(rejected=False)

        return render_template('pendingReq.html', requests=requests, type=type)


@app.route('/pending_request/req_details/<int:req_id>', methods=['GET', 'POST'])
def reqDetails(req_id):
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        type = 'ngo'
        request = Request.query.get_or_404(req_id)
        return render_template('reqDetails.html', request=request, type=type)


@app.route('/accepted/<int:req_id>', methods=['GET', 'POST'])
def accepted(req_id):
    if not session.get('ngo_id'):
        abort(403)
    else:
        request = Request.query.get_or_404(req_id)
        ngo=Ngo.query.get_or_404(session['ngo_id'])
        rprt = Report.query.filter_by(ngo_id=session['ngo_id']).filter_by(medicine_name=request.medicine_name).first()
        if rprt:
            rprt.quantity = rprt.quantity - request.quantity
            rprt.ngo_name=ngo.ngo_name
            request.accepted = True
            request.donater_ngo_id = session['ngo_id']
            request.rejected_by = None
            request.rejected = False
            db.session.commit()
            flash('Accepted Sucessfully', 'success')
        else:
            rpt = Report(ngo_id=session['ngo_id'], medicine_name=request.medicine_name, quantity=request.quantity,ngo_name=ngo.ngo_name)
            request.accepted = True
            request.donater_ngo_id = session['ngo_id']
            request.rejected_by = None
            request.rejected = False
            db.session.add(rpt)
            db.session.commit()
            flash('Accepted Sucessfully', 'success')

        return redirect(url_for('pendingRequest'))


@app.route('/pending_donation_request', methods=['GET', 'POST'])
def pendingDonationRequest():
    if not session.get('ngo_id'):
        abort(403)
    else:
        type = 'ngo'
        donations = db.session.query(Donate).filter_by(receiver_ngo_id=session['ngo_id']).filter_by(
            accepted=False).filter_by(rejected=False)
        return render_template('pendingDonationReq.html', donations=donations, type=type)


@app.route('/pending_donation_request/req_details/<int:don_id>', methods=['GET', 'POST'])
def pendingDonationDetails(don_id):
    if not session.get('ngo_id'):
        abort(403)
    else:
        type = 'ngo'
        donation = Donate.query.get_or_404(don_id)
        user = User.query.get_or_404(donation.donater_user_id)
    return render_template('pendingReqDetails.html', donation=donation, user=user, type=type)


@app.route('/accepted_donation_req/<int:don_id>', methods=['GET', 'POST'])
def acceptPendingReq(don_id):
    if not session.get('ngo_id'):
        abort(403)
    else:
        donation = Donate.query.get_or_404(don_id)
        donation.accepted = True
        db.session.commit()
        donation2 = Donate.query.get_or_404(don_id)
        ngo=Ngo.query.get_or_404(session['ngo_id'])
        rprt = Report.query.filter_by(ngo_id=session['ngo_id']).filter_by(medicine_name=donation2.medicine_name).first()
        if rprt:
            rprt.quantity = rprt.quantity + donation2.quantity
            rprt.ngo_name=ngo.ngo_name
            donation2.accepted = True
            donation2.rejected = False
            donation2.rejected_by = None
            donation2.receiver_ngo_id = session['ngo_id']
            db.session.commit()
            flash('Accepted Sucessfully', 'success')
        else:
            rpt = Report(ngo_id=session['ngo_id'], medicine_name=donation2.medicine_name, quantity=donation2.quantity,ngo_name=ngo.ngo_name)
            donation2.accepted = True
            donation2.rejected = False
            donation2.rejected_by = None
            donation2.receiver_ngo_id = session['ngo_id']
            db.session.add(rpt)
            db.session.commit()
            flash('Accepted Sucessfully', 'success')
        return redirect(url_for('pendingDonationRequest'))


@app.route('/pending_donation_request/req_details/reject_donation/<int:don_id>', methods=['GET', 'POST'])
def rejectDonation(don_id):
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    form = RejectedForm()
    type = 'ngo'
    if form.validate_on_submit():
        donation = Donate.query.get_or_404(don_id)
        donation.rejected = True
        donation.comment = form.comment.data
        donation.rejected_by = session['ngo_id']
        db.session.commit()
        flash('Donation Request Rejected Sucessfully', 'info')
        return redirect(url_for('pendingDonationRequest'))
    return render_template('reject_donation.html', form=form, type=type)


@app.route('/pending_request/req_details/reject_request/<int:req_id>', methods=['GET', 'POST'])
def rejectRequest(req_id):
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    form = RejectedForm()
    type = 'ngo'
    if form.validate_on_submit():
        request = Request.query.get_or_404(req_id)
        request.rejected = True
        request.comment = form.comment.data
        request.rejected_by = session['ngo_id']
        db.session.commit()
        flash('Request Rejected Sucessfully', 'info')
        return redirect(url_for('pendingRequest'))
    return render_template('reject_request.html', form=form, type=type)


@app.route('/donation_history', methods=['GET', 'POST'])
def donationHistory():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        donations = Donate.query.filter_by(donater_user_id=session['user_id']).all()
        type = 'user'
        return render_template('all_donation_history.html', donations=donations, type=type)


@app.route('/donation_history/detail/<int:don_id>', methods=['GET', 'POST'])
def donationHistoryDetail(don_id):
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        type = 'user'
        donation = Donate.query.get_or_404(don_id)
        ngo = Ngo.query.get_or_404(donation.receiver_ngo_id)
        reject_by = Ngo.query.get(donation.rejected_by)
    return render_template('donation_history_details.html', donation=donation, reject_by=reject_by, ngo=ngo, type=type)


@app.route('/request_history', methods=['GET', 'POST'])
def requestHistory():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(requester_user_id=session['user_id']).all()
        type = 'user'
        return render_template('all_request_history.html', requests=requests, type=type)


@app.route('/request_history/detail/<int:req_id>', methods=['GET', 'POST'])
def requestHistoryDetail(req_id):
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        type = 'user'
        request = Request.query.get_or_404(req_id)
        ngo = Ngo.query.get(request.donater_ngo_id)
        reject_by = Ngo.query.get(request.rejected_by)
    return render_template('request_history_details.html', request=request, ngo=ngo, reject_by=reject_by, type=type)


@app.route('/donation_history/all_accepted', methods=['GET', 'POST'])
def allAcceptedDonation():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        donates = Donate.query.filter_by(accepted=True).filter_by(donater_user_id=session['user_id'])
        type = 'user'
        return render_template('all_accepted_donation.html', type=type, donates=donates)


@app.route('/donation_history/all_pending', methods=['GET', 'POST'])
def allPendingDonation():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        donates = Donate.query.filter_by(accepted=False).filter_by(rejected=False).filter_by(
            donater_user_id=session['user_id'])
        type = 'user'
        return render_template('all_pending_donation.html', type=type, donates=donates)


@app.route('/donation_history/all_rejected', methods=['GET', 'POST'])
def allRejectedDonation():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        donates = Donate.query.filter_by(rejected=True).filter_by(donater_user_id=session['user_id'])
        type = 'user'
        return render_template('all_rejected_donation.html', type=type, donates=donates)


@app.route('/request_history/all_accepted_req', methods=['GET', 'POST'])
def requestAcceptedRequest():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(accepted=True).filter_by(requester_user_id=session['user_id'])
        type = 'user'
        return render_template('all_accepted_request.html', type=type, requests=requests)


@app.route('/request_history/all_pending', methods=['GET', 'POST'])
def requestPendingRequest():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(accepted=False).filter_by(rejected=False).filter_by(
            requester_user_id=session['user_id'])
        type = 'user'
        return render_template('all_pending_request.html', type=type, requests=requests)


@app.route('/request_history/all_rejected', methods=['GET', 'POST'])
def requestRejectedRequest():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(rejected=True).filter_by(requester_user_id=session['user_id'])
        type = 'user'
        return render_template('all_rejected_request.html', type=type, requests=requests)


@app.route('/refill_request/<int:req_id>', methods=['GET', 'POST'])
def refillRequest(req_id):
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        type = 'user'
        form = RefillRequestForm()
        if form.validate_on_submit():
            request = Request.query.get_or_404(req_id)
            if form.prescription.data:
                prescription_file = save_prescription(form.prescription.data)
                request.prescription = prescription_file
            request.medicine_name = form.medicine_name.data
            request.doctor_name = form.doctor_name.data
            request.quantity = form.quantity.data
            request.rejected = False
            request.rejected_by = None
            db.session.commit()
            flash('Your request resended successfully', 'success')
            return redirect(url_for('requestHistory'))
        elif reqqq.method == 'GET':
            request = Request.query.get_or_404(req_id)
            form.medicine_name.data = request.medicine_name
            form.quantity.data = request.quantity
            form.doctor_name.data = request.doctor_name

        image_file = url_for('static', filename='presc/' + request.prescription)
        return render_template('refill_request.html', image_file=image_file, form=form, type=type)


@app.route('/refill_donation_request/<int:don_id>', methods=['GET', 'POST'])
def refillDonationRequest(don_id):
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        type = 'user'
        form = RefillDonationForm()
        if form.validate_on_submit():
            donate = Donate.query.get_or_404(don_id)
            if form.medicine_img.data:
                med_img = save_medicine_img(form.medicine_img.data)
                donate.medicine_img = med_img
            donate.medicine_name = form.medicine_name.data
            donate.quantity = form.quantity.data
            donate.receiver_ngo_id = form.ngo.data
            donate.rejected = False
            donate.rejected_by = None
            db.session.commit()
            flash('Your request resended successfully', 'success')
            return redirect(url_for('donationHistory'))
        elif reqqq.method == 'GET':
            donate = Donate.query.get_or_404(don_id)
            form.medicine_name.data = donate.medicine_name
            form.quantity.data = donate.quantity
            form.ngo.data = donate.receiver_ngo_id
        image_file = url_for('static', filename='medicine_img/' + donate.medicine_img)
        return render_template('refill_donation_request.html', image_file=image_file, form=form, type=type)


@app.route('/ndash/donation_history', methods=['GET', 'POST'])
def ngoDonationHistory():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        donations = Donate.query.filter_by(receiver_ngo_id=session['ngo_id']).all()
        type = 'ngo'
        return render_template('ngo_all_donation_history.html', donations=donations, type=type)


@app.route('/ndash/donation_history/detail/<int:don_id>', methods=['GET', 'POST'])
def ngoDonationHistoryDetail(don_id):
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        type = 'ngo'
        donation = Donate.query.get_or_404(don_id)
        if donation.rejected_by == session['ngo_id'] and donation.accepted == False:
            reject = True
        else:
            reject = False
        if donation.receiver_ngo_id == session['ngo_id'] and donation.accepted == False:
            pending = True
        else:
            pending = False
        user = User.query.get_or_404(donation.donater_user_id)
    return render_template('ngo_donation_history_detail.html', donation=donation, user=user, reject=reject, type=type,
                           pending=pending)


@app.route('/ndash/request_history', methods=['GET', 'POST'])
def ngoRequestHistory():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(donater_ngo_id=session['ngo_id']).all()
        type = 'ngo'
        return render_template('ngo_request_history.html', requests=requests, type=type)


@app.route('/ndash/request_history/detail/<int:req_id>', methods=['GET', 'POST'])
def ngoRequestHistoryDetail(req_id):
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        type = 'ngo'
        request = Request.query.get_or_404(req_id)
        user = User.query.get(request.requester_user_id)
        if request.rejected_by == session['ngo_id']:
            reject = True
        else:
            reject = False
    return render_template('ngo_request_history_detail.html', request=request, user=user, reject=reject, type=type)


@app.route('/request_history/ndash/all_accepted_req', methods=['GET', 'POST'])
def ngoAllAcceptedRequest():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        requests = Request.query.filter_by(accepted=True).filter_by(donater_ngo_id=session['ngo_id'])
        type = 'ngo'
        return render_template('ngo_all_accepted_request.html', type=type, requests=requests)


@app.route('/request_history/ndash/all_accepted_don_req', methods=['GET', 'POST'])
def ngoAllAcceptedDonation():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        donations = Donate.query.filter_by(accepted=True).filter_by(receiver_ngo_id=session['ngo_id'])
        type = 'ngo'
        return render_template('ngo_all_accepted_donation.html', type=type, donations=donations)


@app.route('/request_history/ndash/all_pending_don_req', methods=['GET', 'POST'])
def ngoAllPendingDonation():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        donations = Donate.query.filter_by(receiver_ngo_id=session['ngo_id']).filter_by(accepted=False).filter_by(
            rejected=False)
        type = 'ngo'
        return render_template('ngo_all_pending_donation.html', type=type, donations=donations)


@app.route('/request_history/ndash/all_rejected_don_req', methods=['GET', 'POST'])
def ngoAllRejectedDonation():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        donations = Donate.query.filter_by(rejected=True).filter_by(receiver_ngo_id=session['ngo_id'])
        type = 'ngo'
        return render_template('ngo_all_rejected_donation.html', type=type, donations=donations)


@app.route('/ndash/ngo_account', methods=['GET', 'POST'])
def ngoAccount():
    if not session.get('ngo_id'):
        return redirect(url_for('home'))
    else:
        ngo = Ngo.query.get_or_404(session['ngo_id'])
        type = 'ngo'
        return render_template('ngo_account.html', type=type, ngo=ngo)


@app.route('/udash/user_account', methods=['GET', 'POST'])
def userAccount():
    if not session.get('user_id'):
        return redirect(url_for('home'))
    else:
        user = User.query.get_or_404(session['user_id'])
        type = 'user'
        return render_template('user_account.html', type=type, user=user)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def adminDashBoard():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        total_users=db.session.query(User).count()
        total_ngos=db.session.query(Ngo).count()
        data=[total_users,total_ngos]
        return render_template('admin_dashboard.html', type=type,data=data)


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form = LoginForm()
    if session.get('admin_id'):
        return redirect(url_for('adminDashBoard'))
    if form.validate_on_submit():
        # email_id=form.email.data
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and form.password.data == admin.password:
            session['admin_id'] = admin.id
            return redirect(url_for('adminDashBoard'))
        else:
            flash('Login Unsuccessful please check you email id or password', 'danger')
            return redirect(url_for('adminLogin'))
    return render_template('admin_login.html', form=form)


@app.route('/admin_logout', methods=['GET', 'POST'])
def adminlogout():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    session.pop('admin_id', None)
    return redirect(url_for('adminLogin'))


@app.route('/not_approved_user', methods=['GET', 'POST'])
def notApprovedUsers():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        users = User.query.filter_by(is_verified=False).filter_by(rejected=False).filter_by(blocked=False)
        return render_template('admin_not_approved_users.html', type=type, users=users)


@app.route('/not_approved_ngo', methods=['GET', 'POST'])
def notApprovedNgos():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngos = Ngo.query.filter_by(is_verified=False).filter_by(rejected=False).filter_by(blocked=False)
        return render_template('admin_not_approved_ngos.html', type=type, ngos=ngos)


@app.route('/user_account_approved/<int:user_id>', methods=['GET', 'POST'])
def userAccountApproved(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        user = User.query.get_or_404(user_id)
        user.is_verified = True
        db.session.commit()
        flash("user account has been approved", "success")
        return redirect(url_for('notApprovedUsers'))


@app.route('/user_account_rejected/<int:user_id>', methods=['GET', 'POST'])
def userAccountRejected(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        user = User.query.get_or_404(user_id)
        user.rejected=True
        db.session.commit()
        flash("user account has been blocked", "info")
        return redirect(url_for('notApprovedUsers'))


@app.route('/admin_ngo_account_details/<int:ngo_id>', methods=['GET', 'POST'])
def adminNgoAccDetails(ngo_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngo = Ngo.query.get_or_404(ngo_id)
        return render_template('admin_ngo_account_details.html', ngo=ngo,type=type)


@app.route('/ngo_account_approved/<int:ngo_id>', methods=['GET', 'POST'])
def ngoAccountApproved(ngo_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngo = Ngo.query.get_or_404(ngo_id)
        ngo.is_verified = True
        db.session.commit()
        flash("Ngo account has been approved", "success")
        return redirect(url_for('notApprovedNgos'))


@app.route('/ngo_account_blocked/<int:ngo_id>', methods=['GET', 'POST'])
def ngoAccountRejected(ngo_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngo = Ngo.query.get_or_404(ngo_id)
        ngo.rejected = True
        db.session.commit()
        flash("Ngo account has been blocked", "info")
        return redirect(url_for('notApprovedNgos'))


@app.route('/admin_dashboard/activated_users', methods=['GET', 'POST'])
def activatedUser():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        users=User.query.filter_by(blocked=False)
        return render_template('admin_activated_users.html', type=type,users=users)


@app.route('/admin_dashboard/blocked_users', methods=['GET', 'POST'])
def blockedUser():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        users=User.query.filter_by(blocked=True)
        return render_template('admin_blocked_users.html', type=type,users=users)


@app.route('/block_user/<int:user_id>', methods=['GET', 'POST'])
def blockingUser(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        user=User.query.get_or_404(user_id)
        user.blocked=True
        db.session.commit()
        flash(f'user blocked successfully', 'info')
        return redirect(url_for('activatedUser'))


@app.route('/unblock_user/<int:user_id>', methods=['GET', 'POST'])
def unblockingUser(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        user=User.query.get_or_404(user_id)
        user.blocked=False
        db.session.commit()
        flash(f'user blocked successfully', 'info')
        return redirect(url_for('blockedUser'))


#edit

@app.route('/admin_dashboard/activated_ngos', methods=['GET', 'POST'])
def activatedNgo():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngos=Ngo.query.filter_by(blocked=False)
        return render_template('admin_activated_ngos.html', type=type,ngos=ngos)


@app.route('/admin_dashboard/blocked_ngos', methods=['GET', 'POST'])
def blockedNgo():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngos=Ngo.query.filter_by(blocked=True)
        return render_template('admin_blocked_ngos.html', type=type,ngos=ngos)


@app.route('/block_ngo/<int:ngo_id>', methods=['GET', 'POST'])
def blockingNgo(ngo_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngo=Ngo.query.get_or_404(ngo_id)
        ngo.blocked=True
        db.session.commit()
        flash(f'Ngo blocked successfully', 'info')
        return redirect(url_for('activatedNgo'))


@app.route('/unblock_ngo/<int:ngo_id>', methods=['GET', 'POST'])
def unblockingNgo(ngo_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngo=Ngo.query.get_or_404(ngo_id)
        ngo.blocked=False
        db.session.commit()
        flash(f'Ngo blocked successfully', 'info')
        return redirect(url_for('blockedNgo'))


@app.route('/admin_dashboard/ngo_stocks', methods=['GET', 'POST'])
def ngoStocks():
    if not session.get('admin_id'):
        return redirect(url_for('adminLogin'))
    else:
        type = "admin"
        ngos=Ngo.query.all()
        ngo_id=flask.request.args.get('ngo_id')
        ngo_name=flask.request.args.get('ngo_name')
        if ngo_id:
            stocks=Report.query.filter_by(ngo_id=ngo_id)
        else:
            stocks=Report.query.all()
            ngo_name=None
        return render_template('admin_ngo_stocks.html', type=type,ngos=ngos,stocks=stocks,ngo_name=ngo_name)


@app.route('/terms_and_conditions', methods=['GET', 'POST'])
def terms():

    return render_template('terms.html')