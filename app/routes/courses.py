from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from app import db
from app.models.course import Course
from app.models.level import Level
from app.models.timetable import Timetable
from app.models.course_offering import CourseOffering


courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/admin/courses"
)


# =========================================================
# LIST COURSES
# =========================================================

@courses_bp.route("/")
@login_required
def index():

    courses = Course.query.order_by(
        Course.code.asc()
    ).all()

    return render_template(
        "admin/courses/index.html",
        courses=courses
    )


# =========================================================
# ADD COURSE
# =========================================================

@courses_bp.route(
    "/add",
    methods=["GET", "POST"]
)
@login_required
def add():

    levels = Level.query.order_by(
        Level.name.asc()
    ).all()

    if request.method == "POST":

        code = request.form.get(
            "code",
            ""
        ).strip().upper()

        title = request.form.get(
            "title",
            ""
        ).strip()

        units = request.form.get(
            "units",
            ""
        ).strip()

        course_type = request.form.get(
            "course_type",
            "Theory"
        ).strip()

        level_id = request.form.get(
            "level_id",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATE COURSE CODE
        # -------------------------------------------------

        if not code:

            flash(
                "Course code is required.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE COURSE TITLE
        # -------------------------------------------------

        if not title:

            flash(
                "Course title is required.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE COURSE UNITS
        # -------------------------------------------------

        try:
            units = int(units)

        except (ValueError, TypeError):

            flash(
                "Course units must be a valid number.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        if units <= 0:

            flash(
                "Course units must be greater than zero.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE LEVEL
        # -------------------------------------------------

        if not level_id:

            flash(
                "Please select a level.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        try:
            level_id = int(level_id)

        except (ValueError, TypeError):

            flash(
                "Invalid level selected.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        level = db.session.get(
            Level,
            level_id
        )

        if not level:

            flash(
                "Selected level does not exist.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        # -------------------------------------------------
        # CHECK DUPLICATE COURSE CODE
        # -------------------------------------------------

        existing_course = Course.query.filter(
            db.func.upper(Course.code) == code
        ).first()

        if existing_course:

            flash(
                "A course with this code already exists.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        # -------------------------------------------------
        # CREATE COURSE
        # -------------------------------------------------

        course = Course(
            code=code,
            title=title,
            units=units,
            course_type=course_type,
            level_id=level.id
        )

        try:

            db.session.add(course)
            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "An error occurred while adding the course.",
                "danger"
            )

            return render_template(
                "admin/courses/add.html",
                levels=levels
            )

        flash(
            "Course added successfully.",
            "success"
        )

        return redirect(
            url_for("courses.index")
        )

    return render_template(
        "admin/courses/add.html",
        levels=levels
    )


# =========================================================
# EDIT COURSE
# =========================================================

@courses_bp.route(
    "/<int:course_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(course_id):

    course = Course.query.get_or_404(
        course_id
    )

    levels = Level.query.order_by(
        Level.name.asc()
    ).all()

    if request.method == "POST":

        code = request.form.get(
            "code",
            ""
        ).strip().upper()

        title = request.form.get(
            "title",
            ""
        ).strip()

        units = request.form.get(
            "units",
            ""
        ).strip()

        course_type = request.form.get(
            "course_type",
            "Theory"
        ).strip()

        level_id = request.form.get(
            "level_id",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATE COURSE CODE
        # -------------------------------------------------

        if not code:

            flash(
                "Course code is required.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE COURSE TITLE
        # -------------------------------------------------

        if not title:

            flash(
                "Course title is required.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE UNITS
        # -------------------------------------------------

        try:
            units = int(units)

        except (ValueError, TypeError):

            flash(
                "Course units must be a valid number.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        if units <= 0:

            flash(
                "Course units must be greater than zero.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        # -------------------------------------------------
        # VALIDATE LEVEL
        # -------------------------------------------------

        if not level_id:

            flash(
                "Please select a level.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        try:
            level_id = int(level_id)

        except (ValueError, TypeError):

            flash(
                "Invalid level selected.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        level = db.session.get(
            Level,
            level_id
        )

        if not level:

            flash(
                "Selected level does not exist.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        # -------------------------------------------------
        # CHECK DUPLICATE COURSE CODE
        # -------------------------------------------------

        existing_course = Course.query.filter(
            db.func.upper(Course.code) == code,
            Course.id != course.id
        ).first()

        if existing_course:

            flash(
                "Another course already uses this code.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        # -------------------------------------------------
        # UPDATE COURSE
        # -------------------------------------------------

        course.code = code
        course.title = title
        course.units = units
        course.course_type = course_type
        course.level_id = level.id

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "An error occurred while updating the course.",
                "danger"
            )

            return render_template(
                "admin/courses/edit.html",
                course=course,
                levels=levels
            )

        flash(
            "Course updated successfully.",
            "success"
        )

        return redirect(
            url_for("courses.index")
        )

    return render_template(
        "admin/courses/edit.html",
        course=course,
        levels=levels
    )


# =========================================================
# DELETE COURSE
# =========================================================

@courses_bp.route(
    "/<int:course_id>/delete",
    methods=["POST"]
)
@login_required
def delete(course_id):

    course = Course.query.get_or_404(
        course_id
    )

    # -----------------------------------------------------
    # CHECK TIMETABLE USAGE
    # -----------------------------------------------------

    timetable_usage = Timetable.query.filter_by(
        course_id=course.id
    ).first()

    if timetable_usage:

        flash(
            "This course cannot be deleted because it is already "
            "used in the timetable. Clear the timetable first.",
            "danger"
        )

        return redirect(
            url_for("courses.index")
        )

    # -----------------------------------------------------
    # CHECK COURSE OFFERING USAGE
    # -----------------------------------------------------

    offering_usage = CourseOffering.query.filter_by(
        course_id=course.id
    ).first()

    if offering_usage:

        flash(
            "This course cannot be deleted because it has a "
            "course offering assigned to it.",
            "danger"
        )

        return redirect(
            url_for("courses.index")
        )

    # -----------------------------------------------------
    # DELETE COURSE
    # -----------------------------------------------------

    try:

        db.session.delete(course)
        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "An error occurred while deleting the course.",
            "danger"
        )

        return redirect(
            url_for("courses.index")
        )

    flash(
        "Course deleted successfully.",
        "success"
    )

    return redirect(
        url_for("courses.index")
    )