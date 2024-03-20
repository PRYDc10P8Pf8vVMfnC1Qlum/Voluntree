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
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    events = get_events(cu)

    hash_fn = hash_from_name("SHA256")
    if request.method == 'POST':
        new_photo = request.files.get('photo')
        new_password = request.form.get('new-password')
        old_password = request.form.get('current-password')
        new_name = request.form.get('name')

        if verify_password_hashed_salted_peppered(current_user, old_password):
            if new_photo is not None and str(new_photo.mimetype) != 'application/octet-stream':
                if isinstance(cu, Organization):
                    new_photo.save('uploads/' + f'{cu.id}.png')
                else:
                    new_photo.save('uploads/' + f'u{cu.id}.png')
            cu.name = new_name
            if new_password:
                cu.password = update_password_hashed_salted_peppered(hash_fn, new_password)
        else:
            flash('Паролі не співпадають!', category='error-password')

        db.session.commit()
        return redirect('/profile')
    return render_template('user.html', user=cu, is_org=isinstance(cu, Organization), events=events, photo=False)

@profile.route('/delete_profile', methods = ['GET', 'POST'])
@login_required
def delete_acc():
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    if isinstance(cu, Organization):
        for ev in cu.events:
            try:
                os.remove(f'uploads/e{ev.id}.png')
            except Exception:
                pass
            db.session.delete(ev)
        user = Organization.query.get(cu.id)
        logout_user()
        try:
            os.remove(f'uploads/{user.id}.png')
        except Exception:
            pass
        db.session.delete(user)
        db.session.commit()
    if isinstance(cu, User):
        for ev in cu.liked_events:
            try:
                os.remove(f'uploads/e{ev.id}.png')
            except Exception:
                pass
            db.session.delete(ev)
        user = User.query.get(cu.id)
        logout_user()
        try:
            os.remove(f'uploads/u{user.id}.png')
        except Exception:
            pass
        db.session.delete(user)
        db.session.commit()
    return redirect('/home')

def get_events(cu):
    if isinstance(cu, Organization):
        events = cu.events
    else:
        events = cu.liked_events
    return events
