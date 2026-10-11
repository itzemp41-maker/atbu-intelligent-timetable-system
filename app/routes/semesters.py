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
from app.models.semester import Semester


semesters_bp = Blueprint(
    "semesters",
    __name__,
    url_prefix="/admin/semesters"
)


# =========================================================
# LIST SEMESTERS
# =========================================================

@semesters_bp.route("/")
@login_required
def index():

    semesters = Semester.query.order_by(
        Semester.name.asc()
    ).all()

    return render_template(
        "admin/semesters/index.html",
        semesters=semesters
    )


# =========================================================
# ADD SEMESTER
# =========================================================

@semesters_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        # -------------------------------------------------
        # Validate name
        # -------------------------------------------------

        if not name:

            flash(
                "Semester name is required.",
                "danger"
            )

            return render_template(
                "admin/semesters/add.html"
            )

        # -------------------------------------------------
        # Check duplicate
        # -------------------------------------------------

        existing = Semester.query.filter(
            db.func.lower(Semester.name) == name.lower()
        ).first()

        if existing:

            flash(
                "A semester with this name already exists.",
                "danger"
            )

            return render_template(
                "admin/semesters/add.html"
            )

        # -------------------------------------------------
        # Create semester
        # -------------------------------------------------

        semester = Semester(
            name=name
        )

        db.session.add(semester)
        db.session.commit()

        flash(
            "Semester added successfully.",
            "success"
        )

        return redirect(
            url_for("semesters.index")
        )

    return render_template(
        "admin/semesters/add.html"
    )


# =========================================================
# EDIT SEMESTER
# =========================================================

@semesters_bp.route(
    "/<int:semester_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(semester_id):

    semester = Semester.query.get_or_404(
        semester_id
    )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        # -------------------------------------------------
        # Validate name
        # -------------------------------------------------

        if not name:

            flash(
                "Semester name is required.",
                "danger"
            )

            return render_template(
                "admin/semesters/edit.html",
                semester=semester
            )

        # -------------------------------------------------
        # Check duplicate
        # -------------------------------------------------

        existing = Semester.query.filter(
            db.func.lower(Semester.name) == name.lower(),
            Semester.id != semester.id
        ).first()

        if existing:

            flash(
                "Another semester already uses this name.",
                "danger"
            )

            return render_template(
                "admin/semesters/edit.html",
                semester=semester
            )

        # -------------------------------------------------
        # Update semester
        # -------------------------------------------------

        semester.name = name

        db.session.commit()

        flash(
            "Semester updated successfully.",
            "success"
        )

        return redirect(
            url_for("semesters.index")
        )

    return render_template(
        "admin/semesters/edit.html",
        semester=semester
    )


# =========================================================
# DELETE SEMESTER
# =========================================================

@semesters_bp.route(
    "/<int:semester_id>/delete",
    methods=["POST"]
)
@login_required
def delete(semester_id):

    semester = Semester.query.get_or_404(
        semester_id
    )

    db.session.delete(semester)
    db.session.commit()

    flash(
        "Semester deleted successfully.",
        "success"
    )

    return redirect(
        url_for("semesters.index")
    )