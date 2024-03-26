# Volontree
Watch in edit mode for correct view. <br />
├── flaskr/ <br />
│   ├── db.py <br />
│   ├── schema.sql <br />
│   ├── auth.py <br />
│   ├── blog.py <br />
│   ├── templates/ <br />
│   │   ├── base.html <br />
│   │   ├── auth/ <br />
│   │   │   ├── login.html <br />
│   │   │   ├── success.html <br />
│   │   │   ├── confirmation.html <br />
│   │   │   ├── register_org.html <br />
│   │   │   └── register_user.html <br />
│   │   ├── search/ <br />
│   │   │   ├── result.html <br />
│   │   │   ├── find.html <br />
│   │   │   └── all_activities.html <br />
│   │   └── event/ <br />
│   │       ├── create.html <br />
│   │       ├── event.html <br />
│   │       └── edit.html <br />
│   └── static/ <br />
│       ├── script.js <br />
│       └── style.css <br />
└── .venv/ <br />


./
└── voluntree/ <br />
    ├── instance/ <br />
    │   └── voluntree.db <br />
    ├── main.py <br />
    ├── uploads/ <br />
    │   └── some images here <br />
    └── website/ <br />
        ├── auth.py <br />
        ├── create_event.py <br />
        ├── event.py <br />
        ├── filter.py <br />
        ├── home.py <br />
        ├── models.py <br />
        ├── profile.py <br />
        ├── static/ <br />
        │   ├── img/ <br />
        │   │   └── and some images here <br />
        │   ├── js/ <br />
        │   │   ├── script.js <br />
        │   │   ├── script_choose.js <br />
        │   │   ├── script_organization copy.js <br />
        │   │   ├── script_organization.js <br />
        │   │   ├── script_volunteer copy.js <br />
        │   │   └── script_volunteer.js <br />
        │   └── styles/ <br />
        │       ├── card.css <br />
        │       ├── style.css <br />
        │       ├── style_activity.css <br />
        │       ├── style_choose.css <br />
        │       ├── style_create_event.css <br />
        │       ├── style_error.css <br />
        │       ├── style_filter.css <br />
        │       ├── style_organization.css <br />
        │       ├── style_success.css <br />
        │       ├── style_user.css <br />
        │       └── style_volunteer.css <br />
        ├── templates/ <br />
        │   ├── activity.html <br />
        │   ├── choose.html <br />
        │   ├── create_event.html <br />
        │   ├── error.html <br />
        │   ├── filter.html <br />
        │   ├── index.html <br />
        │   ├── organisation.html <br />
        │   ├── success.html <br />
        │   ├── user.html <br />
        │   └── volunteer.html <br />
        └── __init__.py <br />
         
<br />
<br />

+---------------------+       +-------------------+       +-------------------+ <br />
| Client-side         |       | Server-side       |       | Database          | <br />
| (Web Browser, etc.) |<----->| Python, JS        |<----->| SQLite, alchemy,  | <br />
| HTML, CSS, JS       |       |                   |       | File system       | <br />
| Frontend            |       |                   |       | HTML, CSS, images | <br />
+---------------------+       +-------------------+       +-------------------+ <br />
                                         |                           | <br />
                                         +--------- Backend ---------+ <br />
Frameworks: <br />
- Flask
- Flaskalchemy/Mongo DB
- Bootstrap


# __init__.py
Function create app creates an application as well as uses the second function to create a database. It imports every model explained below, registers all blueprints, creates a LoginManager instance, and defines the load_user function, which works with AllUsers instances.
main.py
from website import create_app
importing from package-like website function create_app, which is creating everything and runs the app
-----------------------------------------------------------------------------------------------------------------------------------------------
# auth.py
python file that is in charge of authorization of a volunteer as well as an organization (sign-up, login, logout, delete an account)
authentication
@auth.route('/auth', methods = ["GET"])
def choose():
    return render_template("choose.html")
This function renders the template that is responsible for the choice of volunteer or organization and loads further functions in case of making a choice.
 
@auth.route('/auth/volunteer', methods = ["GET", "POST"])
def auth_volunteer():
  	…
authorization for volunteer(both registration and login)
if the user wants to log in, the program checks if the email exists, then if the hashed passwords match (in case of an error, the flash message appears and shows the issue) and only then logins the user and redirects to the home page.
When registering, the user should enter their name, email, password, and confirmation of the password, and if everything is according to the rules and none of these fields is empty, the user is logged in and redirected to the success page. At the same time, the default user photo is saved to uploads using the imported shutil module (by cloning the existing basic photo), and a new member of the volunteer database is created as well as a member of the AllUsers database.
@auth.route('/auth/organisation', methods = ["GET", 'POST'])
def auth_organization():
  	…
authorization for organization(both registration and login)
The login is similar to a volunteer login, and the same requirement needs to be satisfied in order to log in.
The registration requires more data apart from the name of the organization, email, and password, and confirmation password; it also needs a profile description and address. Photo is optional and is saved the same way as with a volunteer; the new member of the Organization database is created, and an AllUsers member is also.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.load_home'))
 
Logging out is pretty simple due to the imported module flask_login, whereby using logout_user we log out the current_user and redirect them to the home page
@auth.route('/delete')
@login_required
def delete():
    cu = Organization.query.get(int(current_user.user_id)) if current_user.is_org else User.query.get(int(current_user.user_id))
    db.session.delete(cu)
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home.load_home'))
 
Deleting users is also not that hard. We are deleting the cu user(defined by the if statement) from the AllUsers database and the current user from the needed database. Then, committing, logging out the user and redirecting to the home page

# create_event.py
Python file to create an event (only available for organization account). Collect data from the form, where the title, email, description, date, time, and tags should be filled out in order to create an event. If something is missing or is put incorrectly, the error will arise. Photo is optional, the default photo will be loaded into upload automatically if nothing is put. Then, an instance of an event is created and committed with all the data given.

# event.py
python file to display the event that was searched for. First, look for the event, and if the user is authorized, then check if the event is liked by current_user. If the event is liked, it is displayed with ‘Вподобано’; otherwise, ‘Вподобати.’ In case the user liked the event, an instance of UserLikedEvents is created. Also, in the end, it returns the total number of likes that the event has.

# filter.py
function filter_event is responsible for the filter search bar. By using the tags, the user can adjust the function to display needed events. The function returns the list of events sorted by the most recent ones that fall in the chosen category. If no tags are selected, the function returns every event possible.
Function filter_events_with_tags refreshes the page and displays the result events.

# home.py
function load_home renders the index.html and passes all organizations as well as user and is_org (return if the user is the organization or not)
function serve uploads takes the filename argument and transports it to uploads folder
function redirect_to takes hrefed argument and redirects users according to this href

# models.py
Is responsible for models for databases:
db = SQLAlchemy()
 
class AllUsers(db.Model, UserMixin):
    '''
    Table to merge organizations and users into one place,
    since both organizations and users are technically users.
    '''
    __tablename__ = 'all_users'
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_org = db.Column(db.Boolean)
 
class Organization(db.Model, UserMixin):
    '''
    Table for storing data about organizations.
    '''
    __tablename__ = 'organization'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    location = db.Column(db.String(150))
    events = db.relationship('Event', back_populates = 'organization')
    description = db.Column(db.String)
 
class Event(db.Model):
    '''
    Table for storing data about events.
    '''
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
    link = db.Column(db.String)
    liked_by = db.relationship('User', secondary='user_liked_events', back_populates='liked_events')
 
class User(db.Model, UserMixin):
    '''
    Table for storing data about users.
    '''
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    liked_events = db.relationship('Event', secondary='user_liked_events', \
                                   back_populates='liked_by')
 
class Hashtag(db.Model):
    '''
    Table for storing a list of event hashtags.
    '''
    __tablename__ = 'hashtags'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship("Event", secondary = 'event_hashtag', back_populates = 'hashtags')
 
class EventHashtag(db.Model):
    '''
    Table needed to implement many-to-many relationship
    between events and hashtags, since one event can have many hashtags
    and one hashtag can have many events.
    '''
    __tablename__ = 'event_hashtag'
 
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)
 
class UserLikedEvents(db.Model):
    '''
    Table needed to implement many-to-many relationship
    between users and events, since one user can like many events and one
    event can have many users who liked it.
    '''
    __tablename__ = 'user_liked_events'
 
    user_id = db.Column(db.String(10), db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
 
 
# profile.py
function get_profile loads the user’s profile, showing them the current data that they put in the registration form, and also enables them to change some data, such as name, password, and photo, only if the password is set correctly.
Function delete_acc is deleting the current_user instance of AllUsers as well as User or Organization, depending on the type of account. Also, the photo is removed from uploads.
Function get_events intakes a user (User or Organization) and return the liked events(for User) and org events (if Organization)

templates folder
---------------

# index.html
This is the home page of the website. It consists of a navigation bar, which contains four buttons. “Волонтерство” transfers you to the filter.html; “Про платформу” transfers you to the middle part of the page, where is all the information about our platform; “Команда” transfers you to the bottom of the page, where the members of our team are listed.
The “Sign in \ Sign up” button is changed by the “Profile” button when the user is registered.
{% if not user.is_authenticated %}
   <a href="/auth" class="login-button sign-in">Sign In / Sign Up</a>
{% else %}
   <a href="/profile" class="login-button sign-in">Profile</a>
   <a href="/logout" class="login-button sign-up">Log Out</a>
{% endif %}

# choose.html
On this page, a user who is signing in or signing up on our platform can choose whether they are an organization or a volunteer. According to that, they get navigated on an organization registration page or a volunteer one. 

# volunteer.html
The volunteer registration page has two options: sign in and sign up. In the sign-in option, the user has to enter their email address and password. On the other hand, in the signup option, the user has to enter their username and email and create and reenter a password. Also, if one of the required data is not entered, an error pops up.

# organization.html
Organization registration has the same options as the volunteer one, but the signup process, apart from email and password, involves entering an organization name, a description of the organization, their address, and logo. Every input field is required to have data for a successful registration.

# user.html
The user profile page, where they can see their present information and the events that they have given before. Also, they are able to edit their profile if they fancy doing so. Yet the information can be changed only if the password is set correctly. Furthermore, for organization accounts the button add event is available, which redirects them to create_event.html

# create_event.html
Is the page that enables organizations to create events. Every field, except for photos, should be filled with correct information in order for it to be published. There are several fields, namely name, contact email, description, data, time, where it will take place, address(if it is offline) and link(if it is online), also tags(in order for it to be found) and optional photo. if every piece of information is correctly put the event will be created.

# filter.html
Users can get navigated to this page from the home page. Here, they have a drop-down menu “Оберіть теги” with various volunteering categories. After checking the checkboxes with the desired categories, the user presses the “Фільтрувати” button and sees all the available events with checked categories. 
{% if events %}
{% for ev in events %}
{% set truncated_string = (ev.name + ': ' + ev.description)[:77] %}
{% set last_space_index = truncated_string.rfind(' ') %}
The code above checks if the events with matching categories are present. If there are no matches, no events are displayed. 

# activity.html
The user can get to this page from the filter page. Here, they can get additional information about the event, such as the location, the date, and the description. Also, a volunteer can like the event using the “Вподобати” button, which moves the event to their profile, the “Мої події” section. An organization cannot like another organization’s event. 

# success.html
This page shows up after a successful sign-up.

# error.html
This page shows up when an incorrect URL is requested.
