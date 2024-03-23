from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user, AnonymousUserMixin
from .models import Event, Organization, Hashtag, EventHashtag, db, User, UserLikedEvents
import os

event = Blueprint("event", __name__)

@event.route("/event/<string:eventname>", methods = ["GET", "POST"])
@login_required
def event_page(eventname):
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    if isinstance(cu, AnonymousUserMixin):
        return redirect('/auth')
    event_ = Event.query.filter_by(name=eventname).first()
    liked = False
    if isinstance(cu, User):
        liked = event_ in cu.liked_events
    if request.method == 'POST':
        if isinstance(cu, User):
            print(request.form)
            if event_ not in cu.liked_events:
                rel = UserLikedEvents(user_id = cu.id, event_id = event_.id)
                db.session.add(rel)
                db.session.commit()
                liked = True
            else:
                # rel = UserLikedEvents(user_id = current_user.id, event_id = event_.id)
                rel = UserLikedEvents.query.filter_by(user_id=cu.id, event_id=event_.id).first()
                if rel:
                    db.session.delete(rel)
                    db.session.commit()
                    liked = False
    likes_amount = len([k for k in User.query.all() if event_ in k.liked_events])
    print([k.name for k in User.query.all() if event_ in k.liked_events])
    return render_template('activity.html', event=event_, user=cu, is_org=isinstance(cu, Organization), liked=liked, likes = likes_amount)

@event.route('/create_email/<path:to>')
def create_email(to):
    return redirect('https://mail.google.com/mail/?view=cm&to='+to)
