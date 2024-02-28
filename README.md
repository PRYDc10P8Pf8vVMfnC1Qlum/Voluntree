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


