from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # -------------------------------------------------
    # Application Configuration
    # -------------------------------------------------

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "timetable-atbu-development-key"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/timetable_atbu"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # -------------------------------------------------
    # Import Models
    # -------------------------------------------------

    from app.models import (
        User,
        Department,
        Programme,
        Level,
        Lecturer,
        Course,
        Semester,
        Venue,
        TimeSlot,
        Timetable
    )

    # -------------------------------------------------
    # User Loader
    # -------------------------------------------------

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # -------------------------------------------------
    # Create Database Tables
    # -------------------------------------------------

    with app.app_context():
        db.create_all()

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/admin")

    from app.routes.departments import departments_bp
    app.register_blueprint(departments_bp)


    from app.routes.programmes import programmes_bp
    app.register_blueprint(programmes_bp)

   
    from app.routes.levels import levels_bp
    app.register_blueprint(levels_bp)


    from app.routes.courses import courses_bp
    app.register_blueprint(courses_bp)

    from app.routes.lecturers import lecturers_bp
    app.register_blueprint(lecturers_bp)

    from app.routes.venues import venues_bp
    app.register_blueprint(venues_bp)


    from app.routes.time_slots import time_slots_bp
    app.register_blueprint(time_slots_bp)

    from app.routes.semesters import semesters_bp
    app.register_blueprint(semesters_bp)

    from app.routes.timetable import timetable_bp
    app.register_blueprint(timetable_bp)

    from app.routes.course_offerings import course_offerings_bp
    app.register_blueprint(course_offerings_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app