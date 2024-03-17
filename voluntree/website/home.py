from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization, db
# from . import db
# import json

home = Blueprint("home", __name__)

# @login_required
@home.route("/", methods = ["GET","POST"])
def load_home():
    organizations = [Organization.query.all()[k] for k in range(min(6, len(Organization.query.all())))]
    return render_template('index.html', organizations=organizations)
