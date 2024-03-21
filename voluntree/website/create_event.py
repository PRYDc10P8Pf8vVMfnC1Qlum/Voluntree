import shutil
import re
from datetime import datetime, timedelta
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
        error_status = False

        # Check if at least tomorrow
        event_date = datetime.strptime(date, '%Y-%m-%d')
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        if event_date < tomorrow:
            flash('Event date must be at least tomorrow!', category='error-event')
            error_status = True

        # Check if at most 2034 year
        max_date = datetime(2034, 12, 31)
        if event_date > max_date:
            flash('Event date must be at most in 2034!', category='error-event')
            error_status = True

        # Check for tags
        if not checked_boxes:
            flash('You have to pick a tag/tags!', category='error-event')
            error_status = True

        link = request.form.get('link','')
        location = f'{request.form.get("city")}, {request.form.get("address")}' if request.form.get('format_off') == 'on' else "Дистанційно"

        # Check for valid link
        if request.form.get('format_off') != 'on' and not re.match(r'^https://', link):
            flash('Provided link is invalid or not secure!', category='error-event')
            error_status = True

        # Check for link existance
        if request.form.get('format_off') != 'on' and not link:
            flash('You have to provide link for online event!', category='error-event')
            error_status = True

        # Check for address
        if request.form.get('format_off') == 'on' and (not request.form.get("city") and request.form.get("address")):
            flash('You have to provide correct address!', category='error-event')
            error_status = True

        # Show all errors
        if error_status:
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
    return render_template('create_event.html')
