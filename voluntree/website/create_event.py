from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Event, Organization
# from . import db
# import json

create_event = Blueprint("create_event", __name__)

# @login_required
@create_event.route("/create_event", methods = ["POST"])
def create_an_event():
    if request.method == 'POST':
        file = request.files['photo']
        file.save('uploads/' + 'test.png')
        print(request.form, request.files)
        return render_template('index.html')
    return render_template('create_event.html', user = current_user)
