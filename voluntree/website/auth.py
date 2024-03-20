import shutil
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User, Organization, AllUsers
from re import match
# from werkzeug.security import generate_password_hash, check_password_hash
from .models import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
# from .__init__ import email, app
import hashlib, base64, secrets, hmac


auth = Blueprint('auth', __name__)



"""Hashed"""
#https://www.upgrad.com/blog/sha-256-algorithm/ - SHA256 - explained

def hash_name(hash_fn) -> str:
    if hash_fn.name == "SHA256":
        return "SHA256"
    return 0


def hash_from_name(name: str):
    if name == "SHA256":
        def hash_fn(b: bytes) -> bytes:
            return hashlib.sha256(b).digest()

        hash_fn.name = "SHA256"
        return hash_fn
    return 0


def hash_str_and_b64_encode(hash_fn, password: str) -> str:
    pw_bytes = password.encode("utf-8")
    hash_bytes = hash_fn(pw_bytes)
    hash_bytes = base64.b64encode(hash_bytes)
    hashed_password = hash_bytes.decode("ascii")
    return hashed_password

def gen_salt() -> str:
    return secrets.token_urlsafe(20)

def get_global_pepper() -> str:
    """
    Get the global secret pepper from secure memory.
    The important thing is that it is NOT stored in the database.
    """
    return "giveusmaxgradepls"


def update_password_hashed_salted_peppered(hash_fn, password: str) -> None:
    salt = gen_salt()
    pepper = get_global_pepper()
    hashed_password = hash_str_and_b64_encode(hash_fn, pepper + salt + password)
    name = hash_name(hash_fn)
    password_hash =  f"{name}${salt}${hashed_password}"
    return password_hash

def verify_password_hashed_salted_peppered(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split("$")
    pepper = get_global_pepper()
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, pepper + salt + password)

    if not hmac.compare_digest(hashed_password, h):
        return False
    return True



@auth.route('/auth', methods = ["GET"])
def choose():
    return render_template("choose.html")

@auth.route('/auth/volunteer', methods = ["GET", "POST"])
def auth_volunteer():
    
    if request.method == 'POST':
        
        name = request.form.get('name-register')
        # print(request.form)
        if name is None:
            # print('login')
            email = request.form.get('mail-login')
            password = request.form.get('password-login')

            user = User.query.filter_by(email=email).first()
            all_user = AllUsers.query.filter_by(user_id = user.id).first()
            if user:
                if verify_password_hashed_salted_peppered(user, password): # if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(all_user, remember=True)
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
                # print('pass')
                flash('Passwords don\'t match.', category='error-reg')
            elif not bool(match(r'[\w]{7}+', password)):
                flash('Password must be at least 7 characters and contain only letter and numbers', category='error-reg')
            elif not bool(match(r'^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$',email)):
                flash('Incorrect email is given.', category='error-reg')
            elif len(name)<3:
                 flash('Name must at least 3 characters.', category='error-reg')
            else:
                hash_fn = hash_from_name("SHA256")
                password_hash = update_password_hashed_salted_peppered(hash_fn,password)
                print(password_hash)
                new_user = User(email=email, name=name, password=password_hash)
                db.session.add(new_user)
                db.session.commit()

                new_all_user = AllUsers(is_org = False, user_id = new_user.id)
                db.session.add(new_all_user)
                db.session.commit()
                print(new_user.password)
                
                shutil.copy('website\\static\\img\\partner.png', f'uploads\\u{new_user.id}.png')
                login_user(new_all_user, remember=True)

                # flash('Account created!', category='success')
                print('redirecting')
                print()
                cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
                return render_template("success.html", user = cu)

    return render_template("volunteer.html")


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
            all_user = AllUsers.query.filter_by(user_id = user.id).first()
            if user:
                if verify_password_hashed_salted_peppered(user, password): # if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(all_user, remember=True)
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
            logo = request.files.get('logo')
            print(logo.mimetype)
            description = request.form.get('orgname')
            organization = Organization.query.filter_by(email=email).first()
            location = request.form.get('org-adress')

            if organization:
                flash('Email already exists.', category='error-reg')
            elif len(name)<3:
                flash('Name must be at least 3 characters', category='error-reg')
            elif len(description)<24:
                flash('Organization description must be at least 24 characters', category='error-reg')
            # elif len(orgname)<3:
            #     flash('Organization name must be at least 3 characters', category='error-reg')
            elif str(logo.mimetype) == 'application/octet-stream':
                flash('Logo must be provided in order to register', category='error-reg')
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
                hash_fn = hash_from_name("SHA256")
                password_hash = update_password_hashed_salted_peppered(hash_fn,password)
                new_user = Organization(
                    name = name,
                    email = email,
                    password = password_hash,
                    location = location,
                    description = description)
                db.session.add(new_user)
                db.session.commit()
                new_all_user = AllUsers(user_id=new_user.id, is_org = True )
                db.session.add(new_all_user)
                db.session.commit()
                
                
                logo.save('uploads/' + f'{new_user.id}.png')
                login_user(new_all_user, remember=True)
                flash('Account created!', category='success')
                cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
                return render_template("success.html", user = cu)
            

                

    return render_template("organisation.html")



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
    return redirect(url_for('home.load_home'))

@auth.route('/delete')
@login_required
def delete():
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    db.session.delete(cu)
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home.load_home'))


@auth.route('/auth/success')
@login_required
def success():
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    return render_template("success.html", user = cu)

# @auth.route('/auth/email')
# def email():
#     return render_template("email.html", user = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id)))

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
