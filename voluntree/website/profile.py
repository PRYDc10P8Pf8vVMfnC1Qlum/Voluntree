from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user, AnonymousUserMixin, logout_user
from .models import Event, Organization, EventHashtag, db, User, UserLikedEvents
import os
from .auth import *

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods = ["GET", "POST"])
@login_required
def get_profile():
    hash_fn = hash_from_name("SHA256")
    events = get_events(current_user)
    if request.method == 'POST':
        new_photo = request.files.get('photo')
        new_password = request.form.get('new-password')
        old_password = request.form.get('current-password')
        new_name = request.form.get('name')
        if verify_password_hashed_salted_peppered(current_user, old_password):
            if new_photo is not None and str(new_photo.mimetype) != 'application/octet-stream':
                if isinstance(current_user, Organization):
                    new_photo.save('uploads/' + f'{current_user.id}.png')
                else:
                    new_photo.save('uploads/' + f'u{current_user.id}.png')
            current_user.name = new_name
            if new_password:
                current_user.password = update_password_hashed_salted_peppered(hash_fn, new_password)
        db.session.commit()
        return redirect('/profile')
    return render_template('user.html', user=current_user, is_org=isinstance(current_user, Organization), events=events, photo=False)

@profile.route('/delete_profile', methods = ['GET', 'POST'])
@login_required
def delete_acc():
    if isinstance(current_user, Organization):
        for ev in current_user.events:
            try:
                os.remove(f'uploads/e{ev.id}.png')
            except Exception:
                pass
            db.session.delete(ev)
        user = Organization.query.get(current_user.id)
        logout_user()
        try:
            os.remove(f'uploads/{user.id}.png')
        except Exception:
            pass
        db.session.delete(user)
        db.session.commit()
    if isinstance(current_user, User):
        for ev in current_user.liked_events:
            try:
                os.remove(f'uploads/e{ev.id}.png')
            except Exception:
                pass
            db.session.delete(ev)
        user = User.query.get(current_user.id)
        logout_user()
        try:
            os.remove(f'uploads/u{user.id}.png')
        except Exception:
            pass
        db.session.delete(user)
        db.session.commit()
    return redirect('/home')

def get_events(current_user):
    if isinstance(current_user, Organization):
        events = current_user.events
    else:
        events = current_user.liked_events
    return events
