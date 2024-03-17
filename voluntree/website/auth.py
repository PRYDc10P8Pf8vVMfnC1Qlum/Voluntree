from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Organization
from re import match
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/auth', methods = ["GET"])
def choose():
    return render_template("choose.html", user=current_user)

@auth.route('/auth/volunteer', methods = ["GET", "POST"])
def auth_volunteer():
    if request.method == 'POST':
        name = request.form.get('name-register')
        print(request.form)
        if name is None:
            print('login')
            email = request.form.get('mail-login')
            password = request.form.get('password-login')

            user = User.query.filter_by(email=email).first()
            if user:
                if password == user.password: # if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('home.load_home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        else:
            name = request.form.get('name-register')
            email = request.form.get('mail-register')
            password = request.form.get('password-register')
            password_conf = request.form.get('password-register-confirmation')
            print('register')
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error')
            else:
                print('ooooooooooooooo')
                new_user = User(email=email, name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
    return render_template("volunteer.html", user=current_user)




@auth.route('/auth/organisation', methods = ["GET", 'POST'])
def auth_organization():
    if request.method == 'POST':
        name = request.form.get('name-register')
        print(request.form)
        if name is None:
            print('login')
            email = request.form.get('mail-login')
            password = request.form.get('password-login')

            user = Organization.query.filter_by(email=email).first()
            if user:
                if password == user.password: # if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        else:
            name = request.form.get('name-register')
            email = request.form.get('mail-register')
            password = request.form.get('password-register')
            password_conf = request.form.get('password-register-confirmation')
            location = request.form.get('org-adress')
            links = request.form.get('socials')
            description = request.form.get('description')
            logo = request.files.get('photo', False)
            print(request.form)
            print(request.files)
            if not all([name, email, password, password_conf, location, links, description, logo]):
                flash('Field error.', category='error')
            print('register')
            user = Organization.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error')
            else:
                print('ooooooooooooooo')
                new_user = Organization(
                    name = name,
                    email = email,
                    password = password,
                    location = location,
                    links = links,
                    description = description)
                db.session.add(new_user)
                db.session.commit()
                logo.save('uploads/' + f'{new_user.id}.png')
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
    return render_template("organisation.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.load_home'))


# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=first_name, password=generate_password_hash(
#                 password1, method='scrypt'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('views.home'))

#     return render_template("sign_up.html", user=current_user)
