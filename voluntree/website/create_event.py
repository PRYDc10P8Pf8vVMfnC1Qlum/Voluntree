from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event, Organization, Hashtag, EventHashtag, db

create_event = Blueprint("create_event", __name__)

# @login_required HORDEUS DOPILYATY!!! - Yarik
@create_event.route("/create_event", methods = ["GET", "POST"])
def create_an_event():
    if request.method == 'POST':
        title = request.form.get('title')
        email = request.form.get('email')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        checked_boxes = request.form.getlist('tag')
        location = f'{request.form.get("city")}, {request.form.get("address")}' if request.form.get('format_off') == 'on' else "Дистанційно"
        event = Event(
            name = title,
            email = email,
            organization_id = 1, #HORDEUS DOPILYATY!!! - Yarik
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

        file = x if (x:=request.files.get('photo', None)) is not None else event.organization_id
        if not isinstance(file, int):
            file.save('uploads/' + f'e{event.id}.png')
        
        print(request.form, request.files)
        return render_template('index.html')
    return render_template('create_event.html', user = current_user)
