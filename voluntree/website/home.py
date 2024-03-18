from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Organization, db
# from . import db
# import json

home = Blueprint("home", __name__)

# @login_required
@home.route("/", methods = ["GET","POST"])
@home.route("/home", methods = ["GET","POST"])
def load_home():
    organizations = [Organization.query.all()[k] for k in range(min(6, len(Organization.query.all())))]
    return render_template('index.html', organizations=organizations, user=current_user if not isinstance(current_user, AnonymousUserMixin) else False)

@home.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('../uploads', filename)

@home.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404
@home.errorhandler(401)
def unauthorized_page(error):
    return render_template("error.html"), 401
@home.errorhandler(500)
def server_error_page(error):
    return render_template("error.html"), 500
