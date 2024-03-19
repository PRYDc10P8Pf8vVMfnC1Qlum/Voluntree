import shutil
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User, Organization
from re import match
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
# from .__init__ import email, app
import jwt


auth = Blueprint('auth', __name__)


@auth.route('/auth', methods = ["GET"])
def choose():
    return render_template("choose.html")

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
                    flash('Incorrect password, try again.', category='error-log')
            else:
                flash('Email does not exist.', category='error-log')
        else:
            name = request.form.get('name-register')
            email = request.form.get('mail-register')
            password = request.form.get('password-register')
            password_conf = request.form.get('password-register-confirmation')
            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email already exists.', category='error-reg')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error-reg')
            elif not bool(match(r'[\w]{7}+', password)):
                flash('Password must be at least 7 characters and contain only letter and numbers', category='error-reg')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error-reg')
            elif len(name)<3:
                 flash('Name must at least 3 characters.', category='error-reg')
            else:
                new_user = User(email=email, name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                shutil.copy('website\static\img\partner.png', f'uploads/u{new_user.id}.png')
                login_user(new_user, remember=True)
                # flash('Account created!', category='success')
                print('redirecting')
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
            if user:
                if password == user.password: # if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    # login_user(user, remember=True)
                    return redirect(url_for('home.load_home'))
                else:
                    flash('Incorrect password, try again.', category='error-logror')
            else:
                flash('Email does not exist.', category='error-logrror')
        else:
            name = request.form.get('name-register')
            email = request.form.get('mail-register')
            password = request.form.get('password-register')
            password_conf = request.form.get('password-register-confirmation')
            print('register')
            logo = request.files.get('photo')
            print(logo.mimetype)
            description = request.form.get('orgname')
            organization = Organization.query.filter_by(email=email).first()
            location = request.form.get('org-adress')
            links = request.form.get('socials')

            if organization:
                flash('Email already exists.', category='error-reg')
            elif len(name)<3:
                flash('Name must be at least 3 characters', category='error-reg')
            elif len(description)<24:
                flash('Organization description must be at least 24 characters', category='error-reg')
            # elif len(orgname)<3:
            #     flash('Organization name must be at least 3 characters', category='error-reg')
            elif not logo:
                flash('Logo must be provided in order to register', category='error-reg')
            elif not links:
                flash('Socials must be provided in order to register', category='error-reg')
            elif not location:
                flash('Location must be provided', category='error-reg')
            elif password != password_conf:
                print('pass')
                flash('Passwords don\'t match.', category='error-reg')
            elif not bool(match(r'[\w]{7}+', password)):
                flash('Password must be at least 7 characters and contain only letter and numbers', category='error-reg')
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
                #########EMAIL##############
                # token = jwt.encode({"email": email}, current_app.config["SECRET_KEY"])
        
                # # Send verification email
                # email.send(
                #     subject="Verify email",
                #     receivers=email,
                #     html_template="email/verify.html",
                #     body_params={
                #         "token": token
                #     }
                # )
                new_user = Organization(email=email, name=name, password=password, links = links, location = location, description = '')
                db.session.add(new_user)
                db.session.commit()
                
                
                logo.save('uploads/' + f'{new_user.id}.png')
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('home.load_home'))
            

                

    return render_template("organisation.html", user=current_user)



# @auth.route("/user", methods = ["GET","POST"])
# @login_required
# def load_user():
#     orgname = request.form.get('orgname')
#     if not orgname:
#         if request.method == 'POST':
#             name = request.form.get('change-name')
#             email = request.form.get('change-mail')
#             password = request.form.get('password-change')
#             password_conf = request.form.get('password-change-confirmation')
#             content = request.form.get('content')

#             if password:
#                 if password != password_conf:
#                     print('pass')
#                     flash('Passwords don\'t match.', category='error')
#                 current_user.password = password
#                 db.session.commit()
#             if email:
#                 if not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
#                     flash('Incorrect email is given.', category='error')
#                 current_user.email = email
#                 db.session.commit()
#             if name:
#                 current_user.name = name
#                 db.session.commit()
#             if content:
#                 current_user.description = content
#                 db.session.commit()
#         else:
#             if request.method == 'POST':
#                 name = request.form.get('change-name')
#                 email = request.form.get('change-mail')
#                 password = request.form.get('password-change')
#                 password_conf = request.form.get('password-change-confirmation')
#                 content = request.form.get('content')
#                 print('register')
#                 logo = request.form.get('logo')
#                 orgname = request.form.get('orgname')
#                 organization = Organization.query.filter_by(email=email).first()
#                 location = request.form.get('org-adress')
#                 links = request.form.get('socials')

#                 if password:
#                     if password != password_conf:
#                         print('pass')
#                         flash('Passwords don\'t match.', category='error')
#                     current_user.password = password
#                     db.session.commit()
#                 if email:
#                     if not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
#                         flash('Incorrect email is given.', category='error')
#                     current_user.email = email
#                     db.session.commit()
#                 if name:
#                     current_user.name = name
#                     db.session.commit()
#                 if content:
#                     current_user.description = content
#                     db.session.commit()
                
#     return render_template('user.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.choose'))

@auth.route('/delete')
@login_required
def delete():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home.load_home'))


@auth.route('/auth/success')
@login_required
def success():
    return render_template("success.html", user = current_user)

@auth.route('/auth/email')
def email():
    return render_template("email.html", user = current_user)

###################EMAIL
# @auth.route("/verify-email/<token>")
# def verify_email(token):
#     data = jwt.decode(token, current_app.config["SECRET_KEY"])
#     email = data["email"]

#     user = User.query.filter_by(email=email).first()
#     user.verified = True
#     db.session.commit()
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
