from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Hashtag, Organization, User
from datetime import datetime

filter_ = Blueprint("filter", __name__)

@filter_.route("/filter", methods = ["GET", "POST"])
def filter_events():
    cu = (Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))) if not isinstance(current_user, AnonymousUserMixin) else False
    selected_tag = request.args.get('tag', False)
    if request.method == 'POST':
        print(request.form)
        checked_boxes = request.form.getlist("tag")
        if not checked_boxes:
            checked_boxes = [k.name for k in Hashtag.query.all()]
        print(checked_boxes)
        # filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes)).all()
        filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes), Event.date > datetime.now()).all()
        print(filtered_events)
        return render_template('filter.html', events=filtered_events, user=cu if not isinstance(cu, AnonymousUserMixin) else False)
    checked_boxes = [k.name for k in Hashtag.query.all()] if not selected_tag else [selected_tag]
    # filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes)).all()
    filtered_events = Event.query.join(Event.hashtags).filter(Hashtag.name.in_(checked_boxes), Event.date > datetime.now()).all()
    return render_template('filter.html', user=cu, events=filtered_events)

@filter_.route("/filter/<tag>", methods=["GET"])
def filter_events_with_tag(tag):
    return redirect(url_for('filter.filter_events', tag=tag))
