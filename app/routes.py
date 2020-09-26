from flask import render_template, url_for, redirect, request, flash
from app import app, db, bcrypt, limiter
from app.models import User, Account, createaccs
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import phonenumbers as pn


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("3/5minutes")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.userpwd, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Feil brukernavn eller passord, vennligst prøv på nytt", 'danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10/day")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        phonenr = pn.parse(form.tlf.data, "NO")
        user = User(username=form.username.data, useremail=form.email.data,
                    userpwd=hashed_password, usertlf= pn.format_number(phonenr, pn.PhoneNumberFormat.NATIONAL), useraddr=form.addr.data)
        db.session.add(user)
        db.session.commit()
        createaccs(user.id)
        db.session.commit()

        flash(f'Brukeren din har blitt registert, du kan nå logge inn!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/editprofile", methods=['GET', 'POST'])
@login_required
def editprofile():
    form = RegistrationForm()
    if form.validate_on_submit():
        phonenr = pn.parse(form.tlf.data, "NO")
        user = User(useremail=form.email.data,
                    usertlf=pn.format_number(phonenr, pn.PhoneNumberFormat.NATIONAL), useraddr=form.addr.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Dine personlige opplysninger har blitt oppdatert', 'success')
        return redirect(url_for('account'))
    return render_template("editprofile.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html')

@app.route("/myaccs")
@login_required
def myaccs():
    return render_template('myaccs.html')

#Bruker redirectes etter for mange feil login forsøk
@app.errorhandler(429)
def ratelimit_handler(e):
    flash("Du har brukt for mange usuksessfulle login forsøk, prøv på nytt om 5 minutter", 'danger')
    return redirect(url_for("index"))
