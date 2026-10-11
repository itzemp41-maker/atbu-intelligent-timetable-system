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

from app.models import (
    CourseOffering,
    Course,
    Lecturer,
    Semester,
    Level
)


course_offerings_bp = Blueprint(
    "course_offerings",
    __name__,
    url_prefix="/admin/course-offerings"
)


# =========================================================
# LIST COURSE OFFERINGS
# =========================================================

@course_offerings_bp.route("/")
@login_required
def index():

    offerings = (
        CourseOffering.query
        .join(CourseOffering.course)
        .order_by(Course.code.asc())
        .all()
    )

    return render_template(
        "admin/course_offerings/index.html",
        offerings=offerings
    )


# =========================================================
# ADD COURSE OFFERING
# =========================================================

@course_offerings_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    courses = Course.query.order_by(
        Course.code.asc()
    ).all()

    lecturers = Lecturer.query.order_by(
        Lecturer.name.asc()
    ).all()

    semesters = Semester.query.order_by(
        Semester.name.asc()
    ).all()

    levels = Level.query.order_by(
        Level.name.asc()
    ).all()

    if request.method == "POST":

        course_id = request.form.get("course_id")
        lecturer_id = request.form.get("lecturer_id")
        semester_id = request.form.get("semester_id")
        level_id = request.form.get("level_id")

        if not all([
            course_id,
            lecturer_id,
            semester_id,
            level_id
        ]):

            flash(
                "All course offering fields are required.",
                "danger"
            )

            return render_template(
                "admin/course_offerings/add.html",
                courses=courses,
                lecturers=lecturers,
                semesters=semesters,
                levels=levels
            )

        # Check duplicate offering
        existing = CourseOffering.query.filter_by(
            course_id=int(course_id),
            lecturer_id=int(lecturer_id),
            semester_id=int(semester_id),
            level_id=int(level_id)
        ).first()

        if existing:

            flash(
                "This course offering already exists.",
                "danger"
            )

            return render_template(
                "admin/course_offerings/add.html",
                courses=courses,
                lecturers=lecturers,
                semesters=semesters,
                levels=levels
            )

        offering = CourseOffering(
            course_id=int(course_id),
            lecturer_id=int(lecturer_id),
            semester_id=int(semester_id),
            level_id=int(level_id)
        )

        db.session.add(offering)
        db.session.commit()

        flash(
            "Course offering added successfully.",
            "success"
        )

        return redirect(
            url_for("course_offerings.index")
        )

    return render_template(
        "admin/course_offerings/add.html",
        courses=courses,
        lecturers=lecturers,
        semesters=semesters,
        levels=levels
    )


# =========================================================
# EDIT COURSE OFFERING
# =========================================================

@course_offerings_bp.route(
    "/<int:offering_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(offering_id):

    offering = CourseOffering.query.get_or_404(
        offering_id
    )

    courses = Course.query.order_by(
        Course.code.asc()
    ).all()

    lecturers = Lecturer.query.order_by(
        Lecturer.name.asc()
    ).all()

    semesters = Semester.query.order_by(
        Semester.name.asc()
    ).all()

    levels = Level.query.order_by(
        Level.name.asc()
    ).all()

    if request.method == "POST":

        course_id = request.form.get("course_id")
        lecturer_id = request.form.get("lecturer_id")
        semester_id = request.form.get("semester_id")
        level_id = request.form.get("level_id")

        if not all([
            course_id,
            lecturer_id,
            semester_id,
            level_id
        ]):

            flash(
                "All fields are required.",
                "danger"
            )

            return render_template(
                "admin/course_offerings/edit.html",
                offering=offering,
                courses=courses,
                lecturers=lecturers,
                semesters=semesters,
                levels=levels
            )

        duplicate = CourseOffering.query.filter(
            CourseOffering.course_id == int(course_id),
            CourseOffering.lecturer_id == int(lecturer_id),
            CourseOffering.semester_id == int(semester_id),
            CourseOffering.level_id == int(level_id),
            CourseOffering.id != offering.id
        ).first()

        if duplicate:

            flash(
                "Another identical course offering already exists.",
                "danger"
            )

            return render_template(
                "admin/course_offerings/edit.html",
                offering=offering,
                courses=courses,
                lecturers=lecturers,
                semesters=semesters,
                levels=levels
            )

        offering.course_id = int(course_id)
        offering.lecturer_id = int(lecturer_id)
        offering.semester_id = int(semester_id)
        offering.level_id = int(level_id)

        db.session.commit()

        flash(
            "Course offering updated successfully.",
            "success"
        )

        return redirect(
            url_for("course_offerings.index")
        )

    return render_template(
        "admin/course_offerings/edit.html",
        offering=offering,
        courses=courses,
        lecturers=lecturers,
        semesters=semesters,
        levels=levels
    )


# =========================================================
# DELETE COURSE OFFERING
# =========================================================

@course_offerings_bp.route(
    "/<int:offering_id>/delete",
    methods=["POST"]
)
@login_required
def delete(offering_id):

    offering = CourseOffering.query.get_or_404(
        offering_id
    )

    # Remove generated timetable entries belonging
    # to this offering's course/lecturer/level/semester
    from app.models import Timetable

    Timetable.query.filter_by(
        course_id=offering.course_id,
        lecturer_id=offering.lecturer_id,
        level_id=offering.level_id,
        semester_id=offering.semester_id
    ).delete()

    db.session.delete(offering)

    db.session.commit()

    flash(
        "Course offering deleted successfully.",
        "success"
    )

    return redirect(
        url_for("course_offerings.index")
    )