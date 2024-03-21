import shutil
from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, AnonymousUserMixin, logout_user
from .models import Event, Organization, Hashtag, EventHashtag, db, User

create_event = Blueprint("create_event", __name__)

@create_event.route("/create_event", methods = ["GET", "POST"])
def create_an_event():
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    if isinstance(cu, AnonymousUserMixin):
        return redirect('/auth')
    if not isinstance(cu, Organization):
        logout_user()
        return redirect('/auth/organisation')
    if request.method == 'POST':
        title = request.form.get('title')
        email = request.form.get('email')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        checked_boxes = request.form.getlist('tag')
        if not checked_boxes:
            flash('You have to pick a tag/tags!', category='error-event')
            return redirect(url_for('create_event.create_an_event'))
        link = request.form.get('link','') #implement in database first
        location = f'{request.form.get("city")}, {request.form.get("address")}' if request.form.get('format_off') == 'on' else "Дистанційно"
        if request.form.get('format_off') != 'on' and not link:
            flash('You have to provide link for online event!', category='error-event')
            return redirect(url_for('create_event.create_an_event'))
        if request.form.get('format_off') == 'on' and (not request.form.get("city") and request.form.get("address")):
            flash('You have to provide correct address!', category='error-event')
            return redirect(url_for('create_event.create_an_event'))
        event = Event(
            name = title,
            email = email,
            organization_id = cu.id,
            location = location,
            date = datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]), int(time.split(':')[0]), int(time.split(':')[1])),
            description = description,
            link = link
        )
        db.session.add(event)
        hashtags = Hashtag.query.filter(Hashtag.name.in_(checked_boxes)).all()
        for h in hashtags:
            eh = EventHashtag(event_id = event.id, hashtag_id = h.id)
            db.session.add(eh)
        db.session.commit()

        file = x if str((x:=request.files.get('photo', None)).mimetype) != 'application/octet-stream' else event.organization_id
        if not isinstance(file, int):
            file.save('uploads/' + f'e{event.id}.png')
        else:
            shutil.copy(f'uploads/{event.organization_id}.png', f'uploads/e{event.id}.png')
        return redirect('/profile')
    else:
        return render_template('create_event.html')
