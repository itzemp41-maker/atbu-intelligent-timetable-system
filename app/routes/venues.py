from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models.venue import Venue


venues_bp = Blueprint(
    "venues",
    __name__,
    url_prefix="/admin/venues"
)


# =========================================================
# VENUES LIST
# =========================================================

@venues_bp.route("/")
def index():

    venues = (
        Venue.query
        .order_by(Venue.name.asc())
        .all()
    )

    return render_template(
        "admin/venues/index.html",
        venues=venues
    )


# =========================================================
# ADD VENUE
# =========================================================

@venues_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        capacity = request.form.get("capacity", "").strip()
        venue_type = request.form.get("venue_type", "").strip()

        if not name:
            flash("Venue name is required.", "danger")
            return render_template("admin/venues/add.html")

        if not capacity:
            flash("Venue capacity is required.", "danger")
            return render_template("admin/venues/add.html")

        try:
            capacity = int(capacity)
        except ValueError:
            flash("Capacity must be a valid number.", "danger")
            return render_template("admin/venues/add.html")

        if capacity <= 0:
            flash("Capacity must be greater than zero.", "danger")
            return render_template("admin/venues/add.html")

        if not venue_type:
            flash("Please select a venue type.", "danger")
            return render_template("admin/venues/add.html")

        existing = Venue.query.filter_by(name=name).first()

        if existing:
            flash("A venue with this name already exists.", "warning")
            return render_template("admin/venues/add.html")

        venue = Venue(
            name=name,
            capacity=capacity,
            venue_type=venue_type
        )

        db.session.add(venue)

        try:

            db.session.commit()

            flash(
                f"Venue '{name}' added successfully.",
                "success"
            )

            return redirect(url_for("venues.index"))

        except Exception as error:

            db.session.rollback()

            flash(
                f"Unable to add venue: {error}",
                "danger"
            )

    return render_template("admin/venues/add.html")


# =========================================================
# EDIT VENUE
# =========================================================

@venues_bp.route("/edit/<int:venue_id>", methods=["GET", "POST"])
def edit(venue_id):

    venue = Venue.query.get_or_404(venue_id)

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        capacity = request.form.get("capacity", "").strip()
        venue_type = request.form.get("venue_type", "").strip()

        if not name or not capacity or not venue_type:

            flash(
                "All venue fields are required.",
                "danger"
            )

            return render_template(
                "admin/venues/edit.html",
                venue=venue
            )

        try:

            capacity = int(capacity)

        except ValueError:

            flash(
                "Capacity must be a valid number.",
                "danger"
            )

            return render_template(
                "admin/venues/edit.html",
                venue=venue
            )

        if capacity <= 0:

            flash(
                "Capacity must be greater than zero.",
                "danger"
            )

            return render_template(
                "admin/venues/edit.html",
                venue=venue
            )

        duplicate = (
            Venue.query
            .filter(
                Venue.name == name,
                Venue.id != venue.id
            )
            .first()
        )

        if duplicate:

            flash(
                "Another venue with this name already exists.",
                "warning"
            )

            return render_template(
                "admin/venues/edit.html",
                venue=venue
            )

        venue.name = name
        venue.capacity = capacity
        venue.venue_type = venue_type

        try:

            db.session.commit()

            flash(
                "Venue updated successfully.",
                "success"
            )

            return redirect(url_for("venues.index"))

        except Exception as error:

            db.session.rollback()

            flash(
                f"Unable to update venue: {error}",
                "danger"
            )

    return render_template(
        "admin/venues/edit.html",
        venue=venue
    )


# =========================================================
# DELETE VENUE
# =========================================================

@venues_bp.route(
    "/delete/<int:venue_id>",
    methods=["POST"]
)
def delete(venue_id):

    venue = Venue.query.get_or_404(venue_id)

    try:

        db.session.delete(venue)
        db.session.commit()

        flash(
            "Venue deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            f"Unable to delete venue: {error}",
            "danger"
        )

    return redirect(url_for("venues.index"))
