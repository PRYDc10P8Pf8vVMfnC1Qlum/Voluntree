from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization
# from . import db
import json

filter = Blueprint("filter", __name__)

@filter.route("/filter", methods = ["GET", "POST"])
def filter():
    return render_template('filter.html')