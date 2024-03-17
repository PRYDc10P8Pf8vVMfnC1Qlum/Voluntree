from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Organization, Hashtag, EventHashtag, db, User, UserLikedEvents
import os

event = Blueprint("event", __name__)

@event.route("/event/<string:eventname>", methods = ["GET", "POST"])
@login_required
def event_page(eventname):
    if isinstance(current_user, AnonymousUserMixin):
        return redirect('/auth')
    event_ = Event.query.filter_by(name=eventname).first()
    liked = False
    if isinstance(current_user, User):
        liked = event_ in current_user.liked_events
    if request.method == 'POST':
        if isinstance(current_user, User):
            print(request.form)
            if event_ not in current_user.liked_events:
                rel = UserLikedEvents(user_id = current_user.id, event_id = event_.id)
                db.session.add(rel)
                db.session.commit()
                liked = True
            else:
                # rel = UserLikedEvents(user_id = current_user.id, event_id = event_.id)
                rel = UserLikedEvents.query.filter_by(user_id=current_user.id, event_id=event_.id).first()
                if rel:
                    db.session.delete(rel)
                    db.session.commit()
                    liked = False
    return render_template('activity.html', event=event_, user=current_user, is_org=isinstance(current_user, Organization), liked=liked)
