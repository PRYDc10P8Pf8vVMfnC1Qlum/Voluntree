from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization
# from . import db
import json

create_event = Blueprint("create_event", __name__)

@create_event.route("/create_event", methods = ["POST"])
@login_required
def create_event():
    return render_template('create_event.html', user = current_user)
