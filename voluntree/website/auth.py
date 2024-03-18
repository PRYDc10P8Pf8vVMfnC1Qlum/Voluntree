import shutil
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Organization
from re import match
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db
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
                    return redirect(url_for('home.load_home')) #redirect(url_for('home.load_home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        else:
            name = request.form.get('name-register')
            email = request.form.get('mail-register')
            password = request.form.get('password-register')
            password_conf = request.form.get('password-register-confirmation')
            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email already exists.', category='error')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error')
            elif not bool(match(r'[\w]{7}+', password)):
                flash('Password must be at least 7 characters and contain only letter and numbers', category='error')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error')
            elif len(name)<3:
                 flash('Name must at least 3 characters.', category='error')
            else:
                new_user = User(email=email, name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                shutil.copy('website\static\img\partner.png', f'uploads/u{new_user.id}.png')
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.success'))
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
            print(user.__dict__)
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
            location = request.form.get('org-adress')
            links = request.form.get('socials')
            description = request.form.get('description')
            logo = request.files.get('logo')
            print(request.form)
            print(request.files)
            print('register')
            user = Organization.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(name)<3:
                flash('Name must be at least 3 characters', category='error')
            elif len(description)<24:
                flash('Organization description must be at least 24 characters', category='error')
            elif not logo:
                flash('Logo must be provided in order to register', category='error')
            elif not links:
                flash('Socials must be provided in order to register', category='error')
            elif not location:
                flash('Location must be provided', category='error')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error')
            elif not bool(match(r'[\w]{7}+', password)):
                flash('Password must be at least 7 characters and contain only letter and numbers', category='error')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error')
            else:
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
                return redirect('/home')
    return render_template("organisation.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.load_home'))


@auth.route('/auth/success')
@login_required
def success():
    return render_template("success.html", user = current_user)

@auth.route('/auth/email')
def email():
    return render_template("email.html", user = current_user)
