from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.programme import Programme
from app.models.department import Department


programmes_bp = Blueprint(
    "programmes",
    __name__,
    url_prefix="/admin/programmes"
)


# =========================================================
# LIST PROGRAMMES
# =========================================================

@programmes_bp.route("/")
@login_required
def index():

    programmes = Programme.query.order_by(
        Programme.name.asc()
    ).all()

    return render_template(
        "admin/programmes/index.html",
        programmes=programmes
    )


# =========================================================
# ADD PROGRAMME
# =========================================================

@programmes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        department_id = request.form.get("department_id", "").strip()

        # -------------------------------------------------
        # Validate programme name
        # -------------------------------------------------

        if not name:

            flash(
                "Programme name is required.",
                "danger"
            )

            return render_template(
                "admin/programmes/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # Validate department
        # -------------------------------------------------

        if not department_id:

            flash(
                "Please select a department.",
                "danger"
            )

            return render_template(
                "admin/programmes/add.html",
                departments=departments
            )

        department = Department.query.get(
            int(department_id)
        )

        if not department:

            flash(
                "Selected department does not exist.",
                "danger"
            )

            return render_template(
                "admin/programmes/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # Check duplicate programme
        # -------------------------------------------------

        existing = Programme.query.filter(
            db.func.lower(Programme.name) == name.lower(),
            Programme.department_id == department.id
        ).first()

        if existing:

            flash(
                "This programme already exists in the selected department.",
                "danger"
            )

            return render_template(
                "admin/programmes/add.html",
                departments=departments
            )

        # -------------------------------------------------
        # Create programme
        # -------------------------------------------------

        programme = Programme(
            name=name,
            department_id=department.id
        )

        db.session.add(programme)
        db.session.commit()

        flash(
            "Programme added successfully.",
            "success"
        )

        return redirect(
            url_for("programmes.index")
        )

    return render_template(
        "admin/programmes/add.html",
        departments=departments
    )


# =========================================================
# EDIT PROGRAMME
# =========================================================

@programmes_bp.route(
    "/<int:programme_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(programme_id):

    programme = Programme.query.get_or_404(
        programme_id
    )

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        department_id = request.form.get(
            "department_id",
            ""
        ).strip()

        # -------------------------------------------------
        # Validate name
        # -------------------------------------------------

        if not name:

            flash(
                "Programme name is required.",
                "danger"
            )

            return render_template(
                "admin/programmes/edit.html",
                programme=programme,
                departments=departments
            )

        # -------------------------------------------------
        # Validate department
        # -------------------------------------------------

        if not department_id:

            flash(
                "Please select a department.",
                "danger"
            )

            return render_template(
                "admin/programmes/edit.html",
                programme=programme,
                departments=departments
            )

        department = Department.query.get(
            int(department_id)
        )

        if not department:

            flash(
                "Selected department does not exist.",
                "danger"
            )

            return render_template(
                "admin/programmes/edit.html",
                programme=programme,
                departments=departments
            )

        # -------------------------------------------------
        # Check duplicate programme
        # -------------------------------------------------

        existing = Programme.query.filter(
            db.func.lower(Programme.name) == name.lower(),
            Programme.department_id == department.id,
            Programme.id != programme.id
        ).first()

        if existing:

            flash(
                "Another programme with this name already exists in the selected department.",
                "danger"
            )

            return render_template(
                "admin/programmes/edit.html",
                programme=programme,
                departments=departments
            )

        # -------------------------------------------------
        # Update programme
        # -------------------------------------------------

        programme.name = name
        programme.department_id = department.id

        db.session.commit()

        flash(
            "Programme updated successfully.",
            "success"
        )

        return redirect(
            url_for("programmes.index")
        )

    return render_template(
        "admin/programmes/edit.html",
        programme=programme,
        departments=departments
    )


# =========================================================
# DELETE PROGRAMME
# =========================================================

@programmes_bp.route(
    "/<int:programme_id>/delete",
    methods=["POST"]
)
@login_required
def delete(programme_id):

    programme = Programme.query.get_or_404(
        programme_id
    )

    # -------------------------------------------------
    # Prevent deletion if levels exist
    # -------------------------------------------------

    if programme.levels:

        flash(
            "This programme cannot be deleted because it has levels assigned to it.",
            "danger"
        )

        return redirect(
            url_for("programmes.index")
        )

    db.session.delete(programme)
    db.session.commit()

    flash(
        "Programme deleted successfully.",
        "success"
    )

    return redirect(
        url_for("programmes.index")
    )