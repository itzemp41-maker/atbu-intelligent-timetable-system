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

from app.models.level import Level
from app.models.programme import Programme


levels_bp = Blueprint(
    "levels",
    __name__,
    url_prefix="/admin/levels"
)


# =========================================================
# LIST LEVELS
# =========================================================

@levels_bp.route("/")
@login_required
def index():

    levels = Level.query.order_by(
        Level.name.asc()
    ).all()

    return render_template(
        "admin/levels/index.html",
        levels=levels
    )


# =========================================================
# ADD LEVEL
# =========================================================

@levels_bp.route(
    "/add",
    methods=["GET", "POST"]
)
@login_required
def add():

    programmes = Programme.query.order_by(
        Programme.name.asc()
    ).all()

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        programme_id = request.form.get(
            "programme_id"
        )

        # -------------------------------------------------
        # Validate level name
        # -------------------------------------------------

        if not name:

            flash(
                "Level name is required.",
                "danger"
            )

            return render_template(
                "admin/levels/add.html",
                programmes=programmes
            )

        # -------------------------------------------------
        # Validate programme
        # -------------------------------------------------

        if not programme_id:

            flash(
                "Please select a programme.",
                "danger"
            )

            return render_template(
                "admin/levels/add.html",
                programmes=programmes
            )

        programme = Programme.query.get(
            int(programme_id)
        )

        if not programme:

            flash(
                "Selected programme does not exist.",
                "danger"
            )

            return render_template(
                "admin/levels/add.html",
                programmes=programmes
            )

        # -------------------------------------------------
        # Check duplicate level
        # -------------------------------------------------

        existing_level = Level.query.filter_by(
            name=name,
            programme_id=programme.id
        ).first()

        if existing_level:

            flash(
                "This level already exists for the selected programme.",
                "danger"
            )

            return render_template(
                "admin/levels/add.html",
                programmes=programmes
            )

        # -------------------------------------------------
        # Create level
        # -------------------------------------------------

        level = Level(
            name=name,
            programme_id=programme.id
        )

        db.session.add(level)
        db.session.commit()

        flash(
            "Level added successfully.",
            "success"
        )

        return redirect(
            url_for("levels.index")
        )

    return render_template(
        "admin/levels/add.html",
        programmes=programmes
    )


# =========================================================
# EDIT LEVEL
# =========================================================

@levels_bp.route(
    "/<int:level_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(level_id):

    level = Level.query.get_or_404(
        level_id
    )

    programmes = Programme.query.order_by(
        Programme.name.asc()
    ).all()

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        programme_id = request.form.get(
            "programme_id"
        )

        # -------------------------------------------------
        # Validate level name
        # -------------------------------------------------

        if not name:

            flash(
                "Level name is required.",
                "danger"
            )

            return render_template(
                "admin/levels/edit.html",
                level=level,
                programmes=programmes
            )

        # -------------------------------------------------
        # Validate programme
        # -------------------------------------------------

        if not programme_id:

            flash(
                "Please select a programme.",
                "danger"
            )

            return render_template(
                "admin/levels/edit.html",
                level=level,
                programmes=programmes
            )

        programme = Programme.query.get(
            int(programme_id)
        )

        if not programme:

            flash(
                "Selected programme does not exist.",
                "danger"
            )

            return render_template(
                "admin/levels/edit.html",
                level=level,
                programmes=programmes
            )

        # -------------------------------------------------
        # Check duplicate
        # -------------------------------------------------

        existing_level = Level.query.filter(
            Level.name == name,
            Level.programme_id == programme.id,
            Level.id != level.id
        ).first()

        if existing_level:

            flash(
                "This level already exists for the selected programme.",
                "danger"
            )

            return render_template(
                "admin/levels/edit.html",
                level=level,
                programmes=programmes
            )

        # -------------------------------------------------
        # Update level
        # -------------------------------------------------

        level.name = name
        level.programme_id = programme.id

        db.session.commit()

        flash(
            "Level updated successfully.",
            "success"
        )

        return redirect(
            url_for("levels.index")
        )

    return render_template(
        "admin/levels/edit.html",
        level=level,
        programmes=programmes
    )


# =========================================================
# DELETE LEVEL
# =========================================================

@levels_bp.route(
    "/<int:level_id>/delete",
    methods=["POST"]
)
@login_required
def delete(level_id):

    level = Level.query.get_or_404(
        level_id
    )

    db.session.delete(level)

    db.session.commit()

    flash(
        "Level deleted successfully.",
        "success"
    )

    return redirect(
        url_for("levels.index")
    )