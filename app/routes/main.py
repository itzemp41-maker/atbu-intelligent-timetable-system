from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.course import Course
from app.models.lecturer import Lecturer
from app.models.venue import Venue
from app.models.time_slot import TimeSlot
from app.models.department import Department
from app.models.programme import Programme
from app.models.level import Level
from app.models.semester import Semester
from app.models.course_offering import CourseOffering
from app.models.timetable import Timetable


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/admin")
@login_required
def admin_dashboard():

    # =====================================================
    # DASHBOARD STATISTICS
    # =====================================================

    department_count = Department.query.count()

    programme_count = Programme.query.count()

    level_count = Level.query.count()

    course_count = Course.query.count()

    lecturer_count = Lecturer.query.count()

    venue_count = Venue.query.count()

    time_slot_count = TimeSlot.query.count()

    semester_count = Semester.query.count()

    course_offering_count = CourseOffering.query.count()

    timetable_count = Timetable.query.count()


    # =====================================================
    # DASHBOARD
    # =====================================================

    return render_template(
        "admin/dashboard.html",

        user=current_user,

        department_count=department_count,

        programme_count=programme_count,

        level_count=level_count,

        course_count=course_count,

        lecturer_count=lecturer_count,

        venue_count=venue_count,

        time_slot_count=time_slot_count,

        semester_count=semester_count,

        course_offering_count=course_offering_count,

        timetable_count=timetable_count
    )