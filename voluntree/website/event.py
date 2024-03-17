from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization, Hashtag, EventHashtag, db, User
import os

event = Blueprint("event", __name__)

@event.route("/event/<string:eventname>", methods = ["GET", "POST"])
@login_required
def event_page(eventname):
    event_ = Event.query.filter_by(name=eventname).first()
    liked = False
    if isinstance(current_user, User):
        liked = event_ in current_user.liked_events
    if request.method == 'POST':
        print(request.form)
        # HORDEUS! Tut maye buty render template with ВПОДОБАНО замість вподобати
    return render_template('activity.html', event=event_, user=current_user, is_org=isinstance(current_user, Organization), liked=liked)
