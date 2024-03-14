from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Organization(db.Model, UserMixin):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    location = db.Column(db.String(150))
    events = db.relationship('Event', back_populates = 'organization')
    links = db.Column(db.String)
    description = db.Column(db.String)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship("Organization", back_populates="events")
    hashtags = db.relationship("Hashtag", secondary = 'event_hashtag', back_populates = 'events')
    location = db.Column(db.String(150))
    date = db.Column(db.Date)
    description = db.Column(db.String)
    liked_by = db.relationship('User', secondary='user_liked_events', back_populates='liked_events')

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    liked_events = db.relationship('Event', secondary='user_liked_events', back_populates='liked_by')


class Hashtag(db.Model):
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    events = db.relationship("Event", secondary = 'event_hashtag', back_populates = 'hashtags')

class EventHashtag(db.Model):
    __tablename__ = 'event_hashtag'

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)

class UserLikedEvents(db.Model):
    __tablename__ = 'user_liked_events'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
