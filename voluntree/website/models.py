'''Database scheme'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Organization(db.Model, UserMixin):
    '''Organizations table'''
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(10))
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    location = db.Column(db.String(150))
    events = db.relationship('Event', back_populates = 'organization')
    links = db.Column(db.String)
    description = db.Column(db.String)

@db.event.listens_for(Organization, "after_insert")
def organization_after_insert(mapper, connection, target):
    '''Add unique_id to organization object after every insertion'''
    unique_id = f'o{target.id}'
    connection.execute(Organization.__table__.update().where(Organization.id == target.id).values({"unique_id": unique_id}))

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
    unique_id = db.Column(db.String(10))
    name = db.Column(db.String)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    liked_events = db.relationship('Event', secondary='user_liked_events', \
                                   back_populates='liked_by')

@db.event.listens_for(User, "after_insert")
def user_after_insert(mapper, connection, target):
    '''Add unique_id to user object after every insertion'''
    unique_id = f'u{target.id}'
    connection.execute(User.__table__.update().where(User.id == target.id).values({"unique_id": unique_id}))

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
