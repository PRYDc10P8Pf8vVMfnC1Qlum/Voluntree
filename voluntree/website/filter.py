from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Event, Organization
# from . import db
# import json

filter = Blueprint("filter", __name__)

@filter.route("/filter", methods = ["POST"])
def filter_events():
    if request.method == 'POST':
        print(request.form)
        filtered_events = []
        return render_template('filter.html', events=filtered_events, user = current_user)
    return render_template('filter.html', user = current_user)
