from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import Venue


venues = Blueprint(
    "venues",
    __name__,
    url_prefix="/admin/venues"
)


@venues.route("/")
@login_required
def index():

    venues = Venue.query.order_by(Venue.name.asc()).all()

    return render_template(
        "venues/index.html",
        venues=venues
    )


@venues.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        capacity = request.form.get("capacity", "").strip()
        venue_type = request.form.get("venue_type", "").strip()


        if not name:
            flash("Venue name is required.", "danger")
            return render_template("venues/add.html")


        if not capacity:
            flash("Venue capacity is required.", "danger")
            return render_template("venues/add.html")


        try:
            capacity = int(capacity)

        except ValueError:
            flash("Capacity must be a valid number.", "danger")
            return render_template("venues/add.html")


        if capacity < 1:
            flash("Capacity must be greater than zero.", "danger")
            return render_template("venues/add.html")


        venue = Venue(
            name=name,
            capacity=capacity,
            venue_type=venue_type
        )

        db.session.add(venue)
        db.session.commit()


        flash("Venue added successfully.", "success")

        return redirect(
            url_for("venues.index")
        )


    return render_template(
        "venues/add.html"
    )