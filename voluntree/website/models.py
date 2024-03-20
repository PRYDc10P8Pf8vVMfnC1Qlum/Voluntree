'''Database scheme'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class AllUsers(db.Model, UserMixin):
    '''All users table'''
    __tablename__ = 'all_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_org = db.Column(db.Boolean)

class Organization(db.Model, UserMixin):
    '''Organizations table'''
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    location = db.Column(db.String(150))
    events = db.relationship('Event', back_populates = 'organization')
    description = db.Column(db.String)

class Event(db.Model):
    '''Event table'''
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
    '''User table'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    liked_events = db.relationship('Event', secondary='user_liked_events', \
                                   back_populates='liked_by')

class Hashtag(db.Model):
    '''Hashtag table'''
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship("Event", secondary = 'event_hashtag', back_populates = 'hashtags')

class EventHashtag(db.Model):
    '''EventHashtag table'''
    __tablename__ = 'event_hashtag'

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)

class UserLikedEvents(db.Model):
    '''UserLikedEvents table'''
    __tablename__ = 'user_liked_events'

    user_id = db.Column(db.String(10), db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
