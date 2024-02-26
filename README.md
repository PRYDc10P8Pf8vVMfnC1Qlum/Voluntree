# Volontree
Watch in edit mode for correct view.
├── flaskr/
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── success.html
│   │   │   ├── confirmation.html
│   │   │   ├── register_org.html
│   │   │   └── register_user.html
│   │   ├── search/
│   │   │   ├── result.html
│   │   │   ├── find.html
│   │   │   └── all_activities.html
│   │   └── event/
│   │       ├── create.html
│   │       ├── event.html
│   │       └── edit.html
│   └── static/
│       ├── script.js
│       └── style.css
└── .venv/



+---------------------+       +-------------------+       +-------------------+
| Client-side         |       | Server-side       |       | Database          |
| (Web Browser, etc.) |<----->| Python, JS        |<----->| SQLite, alchemy,  |
| HTML, CSS, JS       |       |                   |       | File system       |
| Frontend            |       |                   |       | HTML, CSS, images |
+---------------------+       +-------------------+       +-------------------+
                                         |                           |
                                         +--------- Backend ---------+
Frameworks:
- Flask
- Flaskalchemy/Mongo DB
- Bootstrap


