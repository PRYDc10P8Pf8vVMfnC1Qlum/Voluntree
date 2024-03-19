from datetime import datetime
from os import path
from flask import Flask, url_for
from flask_login import LoginManager
from . import models
#email
# from flask_redmail import RedMail

DB_NAME = 'voluntree.db'
#email
# email = RedMail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    models.db.init_app(app)

    #email
    
    # app.config["EMAIL_HOST"] = "localhost"
    # app.config["EMAIL_PORT"] = 587
    # app.config["EMAIL_USER"] = "me@example.com"
    # app.config["EMAIL_PASSWORD"] = "<PASSWORD>"
    # email.init_app(app)
    ####

    from .home import home
    from .auth import auth
    from .event import event
    from .create_event import create_event
    from .filter import filter_
    from .profile import profile

    # app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(create_event, url_prefix='/')
    app.register_blueprint(event, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(filter_, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')

    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.auth_volunteer'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = models.User.query.get(int(id)).unique_id[0]
        if user == 'u':
            return models.User.query.get(int(id))
        if user == 'o':
            return models.Organization.query.get(int(id))
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        models.db.create_all()
#         o1 = models.Organization(
#             name = 'Українська Волонтерська Служба',
#             email = 'change@volunteer.country',
#             password = '32J2GkkMf7',
#             location = 'Одеса',
#             links = 'https://t.me/VolunteerCountry',
#             description = 'Українська Волонтерська Служба — громадська організація, \
# яка розвиває культуру волонтерства та взаємодопомоги в Україні.'
#         )
#         o2 = models.Organization(
#             name = 'БФ "Таблеточки"',
#             email = 'info@tabletochki.org',
#             password = 'R4rL888nXh',
#             location = 'Київ, Омеляновича-Павленка 4/6',
#             links = 'https://tabletochki.org',
#             description = 'Головне завдання «Таблеточок» — зробити так, щоб жодна \
# дитина в Україні не помирала від раку.'
#         )
#         o3 = models.Organization(
#             name = 'Молодь за Мир',
#             email = 'molod.za.myr@gmail.com',
#             password = '9ma25JCUu9',
#             location = 'Київ, Проспект Перемоги 30',
#             links = 'https://www.facebook.com/molod.za.myr',
#             description = 'Молодь за мир — це всесвітній рух молодих людей, \
# створений всередині Спільноти святого Егідія.'
#         )
#         o4 = models.Organization(
#             name = 'Молодіжна громадська організація "UkrTeenScience"',
#             email = 'ukrteenscience@gmail.com',
#             password = 'c5v9Bm8H4E',
#             location = 'Чернігів, Рибакова 57',
#             links = 'https://ukrteenscience.com.ua/?fbclid=\
# IwAR1fVjAqa8kYrEQPmMHRLc4_RzEPMrVR6vx3pP4t1o6aUu5LmZB1zRyMX1M',
#             description = 'Ми - молодіжна громадська організація "UkrTeenScience", \
# що є офіційно зареєстрованим громадським формуванням.'
#         )
#         o5 = models.Organization(
#             name = 'ГО "Сурдо Школа"',
#             email = 'surdo.school.odesa@gmail.com',
#             password = 'x326GnLy9C',
#             location = 'Одеса, вул. Кримська 84',
#             links = 'https://www.facebook.com/surdoschool',
#             description = "Сурдо Школа - це організація, яка просуває \
# ідеї інклюзії та безбар'єрності серед українського суспільства."
#         )
#         e1 = models.Event(
#             name = 'Проведення Шкільного уроку волонтерства від Української Волонтерської Служби',
#             email = 'change@volunteer.country',
#             organization_id = 1,
#             location = 'Вся Україна',
#             date = datetime(2024, 6, 24, 13, 30),
#             description = 'Шкільний урок волонтерства – ініціатива\
#  Української Волонтерської Служби.'
#         )
#         e2 = models.Event(
#             name = 'Волонтерство у проєкті «Мій телефонний друг»',
#             email = 'change@volunteer.country',
#             organization_id = 1,
#             location = 'Дистанційно',
#             date = datetime(2024, 3, 4, 13, 30),
#             description = 'Мій телефонний друг – всеукраїнський проєкт дружньої підтримки людей.'
#         )
#         e3 = models.Event(
#             name = 'Волонтерство у Благодійному фонді «Таблеточки»',
#             email = 'info@tabletochki.org',
#             organization_id = 2,
#             location = 'Київ, Львів',
#             date = datetime(2024, 3, 31, 13, 30),
#             description = 'Приєднуйся до волонтерства у Благодійному фонді «Таблеточки».'
#         )
#         e4 = models.Event(
#             name = 'Пошук музикантів для волонтерства в Молодь за Мир',
#             email = 'molod.za.myr@gmail.com',
#             organization_id = 3,
#             location = 'Львів',
#             date = datetime(2024, 3, 31, 13, 30),
#             description = 'Друзі, якщо ви вмієте грати на музичних інструментах, \
# таких як піаніно чи гітара, ми вас шукаємо!'
#         )
#         e5 = models.Event(
#             name = 'Волонтерство у команді "Молодь за Мир"',
#             email = 'molod.za.myr@gmail.com',
#             organization_id = 3,
#             location = 'Львів',
#             date = datetime(2024, 10, 9, 13, 30),
#             description = 'Ми «Молодь за мир» — рух старшокласників та студентів \
# всередині Спільноти святого Егідія.'
#         )
#         e6 = models.Event(
#             name = 'Долучайся до команди "UkrTeenScience"',
#             email = 'ukrteenscience@gmail.com',
#             organization_id = 4,
#             location = 'Чернігів',
#             date = datetime(2024, 3, 31, 13, 30),
#             description = 'UkrTeenScience - молодіжна громадська організація, \
# яка займається розвитком та популяризацією науки.'
#         )
#         e7 = models.Event(
#             name = 'Шукаємо волонтерів-рекрутерів та HR-спеціалістів у проєкт UkrTeenScience',
#             email = 'ukrteenscience@gmail.com',
#             organization_id = 4,
#             location = 'Чернігів',
#             date = datetime(2024, 11, 1, 13, 30),
#             description = 'МГО UkrTeenScience в пошуку волонтерів-рекрутерів та HR-спеціалістів.'
#         )
#         e8 = models.Event(
#             name = 'СММ-волонтерство в інклюзивній ГО, що допомагає нечуючим українцям',
#             email = 'surdo.school.odesa@gmail.com',
#             organization_id = 5,
#             location = 'Вся Україна',
#             date = datetime(2024, 3, 31, 13, 30),
#             description = "Сурдо Школа - це організація, яка просуває ідеї інклюзії та \
# безбар'єрності серед українського суспільства."
#         )
#         u1 = models.User(
#             name = 'Elon Musk',
#             email = 'elon.musk@gmail.com',
#             password = 'JHKB89ihsdc10'
#         )
#         h1 = models.Hashtag(name = 'Допомога захисникам')
#         h2 = models.Hashtag(name = 'Освіта та наука')
#         h3 = models.Hashtag(name = 'Розвиток міста')
#         h4 = models.Hashtag(name = 'Інтелектуальне волонтерство')
# #         h5 = models.Hashtag(name = 'Регулярне волонтерство')
#         h6 = models.Hashtag(name = 'Донорство крові')
#         h7 = models.Hashtag(name = 'Правозахист')
#         h8 = models.Hashtag(name = 'Волонтерство у пробації')
#         h9 = models.Hashtag(name = 'Спорт')
#         h10 = models.Hashtag(name = 'Онлайн волонтерство')
#         h11 = models.Hashtag(name = 'Волонтерство з ВПО')
#         h12 = models.Hashtag(name = 'Волонтерство на заходах')
#         h13 = models.Hashtag(name = 'Екологія та зоозахист')
#         h14 = models.Hashtag(name = 'Культура та мистецтво')
#         h15 = models.Hashtag(name = 'Міжнародне волонтерство')
#         h16 = models.Hashtag(name = 'Переклади та журналістика')
#         h17 = models.Hashtag(name = 'Психологічна допомога')
#         h18  = models.Hashtag(name = 'Соціальна допомога')
        # eh1 = models.EventHashtag(event_id = 1, hashtag_id = 2)
        # eh2 = models.EventHashtag(event_id = 1, hashtag_id = 3)
        # eh3 = models.EventHashtag(event_id = 1, hashtag_id = 4)
        # eh4 = models.EventHashtag(event_id = 2, hashtag_id = 9)
        # eh5 = models.EventHashtag(event_id = 2, hashtag_id = 16)
        # eh6 = models.EventHashtag(event_id = 2, hashtag_id = 17)
        # eh7 = models.EventHashtag(event_id = 3, hashtag_id = 16)
        # eh8 = models.EventHashtag(event_id = 3, hashtag_id = 11)
        # eh9 = models.EventHashtag(event_id = 4, hashtag_id = 10)
        # eh10 = models.EventHashtag(event_id = 4, hashtag_id = 13)
        # eh11 = models.EventHashtag(event_id = 5, hashtag_id = 10)
        # eh12 = models.EventHashtag(event_id = 6, hashtag_id = 9)
        # eh13 = models.EventHashtag(event_id = 6, hashtag_id = 2)
        # eh14 = models.EventHashtag(event_id = 6, hashtag_id = 4)
        # eh15 = models.EventHashtag(event_id = 7, hashtag_id = 2)
        # eh16 = models.EventHashtag(event_id = 8, hashtag_id = 9)
        # eh17 = models.EventHashtag(event_id = 8, hashtag_id = 17)
        # eh18 = models.EventHashtag(event_id = 8, hashtag_id = 2)
        # eh19 = models.EventHashtag(event_id = 8, hashtag_id = 11)
        # eh20 = models.EventHashtag(event_id = 8, hashtag_id = 4)
        # eh21 = models.EventHashtag(event_id = 8, hashtag_id = 13)
        # eh22 = models.EventHashtag(event_id = 8, hashtag_id = 15)

        # ue1 = models.UserLikedEvents(user_id = 1, event_id = 1)
        # ue2 = models.UserLikedEvents(user_id = 1, event_id = 2)
        # ue3 = models.UserLikedEvents(user_id = 1, event_id = 3)
        # models.db.session.add_all([o1, e1, e2, o2, e3, o3, e4, e5, o4, e6, e7, o5, e8, h1, \
        #     h2, h3, h4, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, u1])
        # models.db.session.add_all([eh1, eh2, eh3, eh4, eh5, eh6, eh7, eh8, eh9, eh10, eh11, eh12, \
        # eh13, eh14, eh15, eh16, eh17, eh18, eh19, eh20, eh21, eh22, ue1, ue2, ue3])
        # models.db.session.commit()
        # print(models.Event.query.first().hashtags)
        print('DB created!')
