from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory, redirect, url_for
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Organization, db, User
from werkzeug.exceptions import HTTPException
# from . import db
# import json

home = Blueprint("home", __name__)

@home.route("/", methods = ["GET","POST"])
@home.route("/home", methods = ["GET","POST"])
def load_home():
    cu = (Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))) if not isinstance(current_user, AnonymousUserMixin) else False
    organizations = [Organization.query.all()[k] for k in range(min(6, len(Organization.query.all())))]
    return render_template('index.html', organizations=organizations, user=cu, is_org=isinstance(cu, Organization))

@home.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('../uploads', filename)

@home.route('/redirect/<path:hrefed>')
def redirect_to(hrefed):
    return redirect(hrefed)
