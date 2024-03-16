from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Event, Organization
# from . import db
# import json

home = Blueprint("home", __name__)

@login_required
@home.route("/", methods = ["GET","POST"])
def load_home():
    return render_template('index.html')
