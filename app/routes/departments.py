from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.department import Department


# =========================================================
# DEPARTMENTS BLUEPRINT
# =========================================================

departments_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/admin/departments"
)


# =========================================================
# LIST DEPARTMENTS
# =========================================================

@departments_bp.route("/")
@login_required
def index():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    return render_template(
        "admin/departments/index.html",
        departments=departments
    )


# =========================================================
# ADD DEPARTMENT
# =========================================================

@departments_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()

        # Validate name
        if not name:

            flash(
                "Department name is required.",
                "danger"
            )

            return render_template(
                "admin/departments/add.html"
            )

        # Check duplicate name
        existing_name = Department.query.filter(
            db.func.lower(Department.name) == name.lower()
        ).first()

        if existing_name:

            flash(
                "A department with this name already exists.",
                "danger"
            )

            return render_template(
                "admin/departments/add.html"
            )

        # Check duplicate code
        if code:

            existing_code = Department.query.filter(
                db.func.upper(Department.code) == code
            ).first()

            if existing_code:

                flash(
                    "A department with this code already exists.",
                    "danger"
                )

                return render_template(
                    "admin/departments/add.html"
                )

        # Create department
        department = Department(
            name=name,
            code=code if code else None
        )

        db.session.add(department)
        db.session.commit()

        flash(
            "Department added successfully.",
            "success"
        )

        return redirect(
            url_for("departments.index")
        )

    return render_template(
        "admin/departments/add.html"
    )


# =========================================================
# EDIT DEPARTMENT
# =========================================================

@departments_bp.route(
    "/<int:department_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(department_id):

    department = Department.query.get_or_404(
        department_id
    )

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()

        # Validate name
        if not name:

            flash(
                "Department name is required.",
                "danger"
            )

            return render_template(
                "admin/departments/edit.html",
                department=department
            )

        # Check duplicate name
        existing_name = Department.query.filter(
            db.func.lower(Department.name) == name.lower(),
            Department.id != department.id
        ).first()

        if existing_name:

            flash(
                "Another department already uses this name.",
                "danger"
            )

            return render_template(
                "admin/departments/edit.html",
                department=department
            )

        # Check duplicate code
        if code:

            existing_code = Department.query.filter(
                db.func.upper(Department.code) == code,
                Department.id != department.id
            ).first()

            if existing_code:

                flash(
                    "Another department already uses this code.",
                    "danger"
                )

                return render_template(
                    "admin/departments/edit.html",
                    department=department
                )

        # Update department
        department.name = name
        department.code = code if code else None

        db.session.commit()

        flash(
            "Department updated successfully.",
            "success"
        )

        return redirect(
            url_for("departments.index")
        )

    return render_template(
        "admin/departments/edit.html",
        department=department
    )


# =========================================================
# DELETE DEPARTMENT
# =========================================================

@departments_bp.route(
    "/<int:department_id>/delete",
    methods=["POST"]
)
@login_required
def delete(department_id):

    department = Department.query.get_or_404(
        department_id
    )

    # Prevent deletion if relationships exist
    if department.lecturers or department.programmes:

        flash(
            "This department cannot be deleted because "
            "it has lecturers or programmes assigned to it.",
            "danger"
        )

        return redirect(
            url_for("departments.index")
        )

    # Delete department
    db.session.delete(department)
    db.session.commit()

    flash(
        "Department deleted successfully.",
        "success"
    )

    return redirect(
        url_for("departments.index")
    )