from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Organization, db
# from . import db
# import json

home = Blueprint("home", __name__)

@home.route("/", methods = ["GET","POST"])
@home.route("/home", methods = ["GET","POST"])
def load_home():
    organizations = [Organization.query.all()[k] for k in range(min(6, len(Organization.query.all())))]
    return render_template('index.html', organizations=organizations, user=current_user if not isinstance(current_user, AnonymousUserMixin) else False)
