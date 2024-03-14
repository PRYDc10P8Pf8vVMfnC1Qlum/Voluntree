from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Hashtag

filter_ = Blueprint("filter", __name__)

@filter_.route("/filter", methods = ["GET", "POST"])
def filter_events():
    if request.method == 'POST':
        print(request.form)
        checked_boxes = request.form.getlist("tag")
        if not checked_boxes:
            checked_boxes = [k.name for k in Hashtag.query.all()]
        print(checked_boxes)
        filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes)).all()
        print(filtered_events)
        return render_template('filter.html', events=filtered_events, user = current_user)
    checked_boxes = [k.name for k in Hashtag.query.all()]
    filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes)).all()
    return render_template('filter.html', user = current_user, events=filtered_events)
