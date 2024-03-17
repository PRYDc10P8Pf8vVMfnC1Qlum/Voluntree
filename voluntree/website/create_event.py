import shutil
from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user, AnonymousUserMixin, logout_user
from .models import Event, Organization, Hashtag, EventHashtag, db

create_event = Blueprint("create_event", __name__)

@create_event.route("/create_event", methods = ["GET", "POST"])
def create_an_event():
    if isinstance(current_user, AnonymousUserMixin):
        return redirect('/auth')
    if not isinstance(current_user, Organization):
        logout_user()
        return redirect('/auth/organisation')
    if request.method == 'POST':
        title = request.form.get('title')
        email = request.form.get('email')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        checked_boxes = request.form.getlist('tag')
        if len(checked_boxes) < 1:
            flash('You have to pick a tag/tags!', category='error')
        link = request.form.get('link','') #implement in database first
        location = f'{request.form.get("city")}, {request.form.get("address")}' if request.form.get('format_off') == 'on' else "Дистанційно"
        event = Event(
            name = title,
            email = email,
            organization_id = current_user.id,
            location = location,
            date = datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]), int(time.split(':')[0]), int(time.split(':')[1])),
            description = description
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
        return redirect('/home')
    else:
        return render_template('create_event.html')
