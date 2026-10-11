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
from app.models.lecturer import Lecturer
from app.models.department import Department


lecturers_bp = Blueprint(
    "lecturers",
    __name__,
    url_prefix="/admin/lecturers"
)


# =========================================================
# LIST LECTURERS
# =========================================================

@lecturers_bp.route("/")
@login_required
def index():

    lecturers = Lecturer.query.order_by(
        Lecturer.name.asc()
    ).all()

    return render_template(
        "admin/lecturers/index.html",
        lecturers=lecturers
    )


# =========================================================
# ADD LECTURER
# =========================================================

@lecturers_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        staff_id = request.form.get(
            "staff_id",
            ""
        ).strip()

        name = request.form.get(
            "name",
            ""
        ).strip()

        department_id = request.form.get(
            "department_id",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATE NAME
        # -------------------------------------------------

        if not name:

            flash(
                "Lecturer name is required.",
                "danger"
            )

            return render_template(
                "admin/lecturers/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # VALIDATE DEPARTMENT
        # -------------------------------------------------

        if not department_id:

            flash(
                "Please select a department.",
                "danger"
            )

            return render_template(
                "admin/lecturers/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # CHECK STAFF ID
        # -------------------------------------------------

        if staff_id:

            existing_staff = Lecturer.query.filter_by(
                staff_id=staff_id
            ).first()

            if existing_staff:

                flash(
                    "A lecturer with this staff ID already exists.",
                    "danger"
                )

                return render_template(
                    "admin/lecturers/add.html",
                    departments=departments
                )

        # -------------------------------------------------
        # CHECK DEPARTMENT
        # -------------------------------------------------

        department = Department.query.get(
            department_id
        )

        if not department:

            flash(
                "Selected department does not exist.",
                "danger"
            )

            return render_template(
                "admin/lecturers/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # CREATE LECTURER
        # -------------------------------------------------

        lecturer = Lecturer(
            staff_id=staff_id if staff_id else None,
            name=name,
            department_id=department.id
        )

        db.session.add(lecturer)
        db.session.commit()

        flash(
            "Lecturer added successfully.",
            "success"
        )

        return redirect(
            url_for("lecturers.index")
        )

    return render_template(
        "admin/lecturers/add.html",
        departments=departments
    )


# =========================================================
# EDIT LECTURER
# =========================================================

@lecturers_bp.route(
    "/<int:lecturer_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(lecturer_id):

    lecturer = Lecturer.query.get_or_404(
        lecturer_id
    )

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        staff_id = request.form.get(
            "staff_id",
            ""
        ).strip()

        name = request.form.get(
            "name",
            ""
        ).strip()

        department_id = request.form.get(
            "department_id",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATE NAME
        # -------------------------------------------------

        if not name:

            flash(
                "Lecturer name is required.",
                "danger"
            )

            return render_template(
                "admin/lecturers/edit.html",
                lecturer=lecturer,
                departments=departments
            )

        # -------------------------------------------------
        # VALIDATE DEPARTMENT
        # -------------------------------------------------

        if not department_id:

            flash(
                "Please select a department.",
                "danger"
            )

            return render_template(
                "admin/lecturers/edit.html",
                lecturer=lecturer,
                departments=departments
            )

        # -------------------------------------------------
        # CHECK DUPLICATE STAFF ID
        # -------------------------------------------------

        if staff_id:

            existing_staff = Lecturer.query.filter(
                Lecturer.staff_id == staff_id,
                Lecturer.id != lecturer.id
            ).first()

            if existing_staff:

                flash(
                    "Another lecturer already uses this staff ID.",
                    "danger"
                )

                return render_template(
                    "admin/lecturers/edit.html",
                    lecturer=lecturer,
                    departments=departments
                )

        # -------------------------------------------------
        # CHECK DEPARTMENT
        # -------------------------------------------------

        department = Department.query.get(
            department_id
        )

        if not department:

            flash(
                "Selected department does not exist.",
                "danger"
            )

            return render_template(
                "admin/lecturers/edit.html",
                lecturer=lecturer,
                departments=departments
            )

        # -------------------------------------------------
        # UPDATE LECTURER
        # -------------------------------------------------

        lecturer.staff_id = (
            staff_id if staff_id else None
        )

        lecturer.name = name

        lecturer.department_id = department.id

        db.session.commit()

        flash(
            "Lecturer updated successfully.",
            "success"
        )

        return redirect(
            url_for("lecturers.index")
        )

    return render_template(
        "admin/lecturers/edit.html",
        lecturer=lecturer,
        departments=departments
    )


# =========================================================
# DELETE LECTURER
# =========================================================

@lecturers_bp.route(
    "/<int:lecturer_id>/delete",
    methods=["POST"]
)
@login_required
def delete(lecturer_id):

    lecturer = Lecturer.query.get_or_404(
        lecturer_id
    )

    db.session.delete(lecturer)

    db.session.commit()

    flash(
        "Lecturer deleted successfully.",
        "success"
    )

    return redirect(
        url_for("lecturers.index")
    )