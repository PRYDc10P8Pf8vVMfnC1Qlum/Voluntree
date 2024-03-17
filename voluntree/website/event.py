from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization, Hashtag, EventHashtag, db
import os

event = Blueprint("event", __name__)

@login_required #HORDEUS DOPILYATY!!! - Yarik
@event.route("/event/<string:eventname>", methods = ["GET", "POST"])
def event_page(eventname):
    if request.method == 'POST':
        pass
        # HORDEUS! Tut maye buty render template with ВПОДОБАНО замість вподобати

    event_ = Event.query.filter_by(name=eventname).first()
    return render_template('activity.html', event=event_, user=current_user)
