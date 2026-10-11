from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.time_slot import TimeSlot


time_slots_bp = Blueprint(
    "time_slots",
    __name__,
    url_prefix="/admin/time-slots"
)


# =========================================================
# LIST TIME SLOTS
# =========================================================

@time_slots_bp.route("/")
@login_required
def index():

    time_slots = TimeSlot.query.order_by(
        TimeSlot.day.asc(),
        TimeSlot.start_time.asc()
    ).all()

    return render_template(
        "admin/time_slots/index.html",
        time_slots=time_slots
    )


# =========================================================
# ADD TIME SLOT
# =========================================================

@time_slots_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        day = request.form.get("day", "").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()

        # Validate required fields
        if not day or not start_time or not end_time:

            flash(
                "All time slot fields are required.",
                "danger"
            )

            return render_template(
                "admin/time_slots/add.html"
            )

        # Prevent identical start and end time
        if start_time >= end_time:

            flash(
                "End time must be later than start time.",
                "danger"
            )

            return render_template(
                "admin/time_slots/add.html"
            )

        # Create time slot
        time_slot = TimeSlot(
            day=day,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(time_slot)
        db.session.commit()

        flash(
            "Time slot added successfully.",
            "success"
        )

        return redirect(
            url_for("time_slots.index")
        )

    return render_template(
        "admin/time_slots/add.html"
    )


# =========================================================
# EDIT TIME SLOT
# =========================================================

@time_slots_bp.route(
    "/<int:time_slot_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(time_slot_id):

    time_slot = TimeSlot.query.get_or_404(
        time_slot_id
    )

    if request.method == "POST":

        day = request.form.get("day", "").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()

        # Validate required fields
        if not day or not start_time or not end_time:

            flash(
                "All time slot fields are required.",
                "danger"
            )

            return render_template(
                "admin/time_slots/edit.html",
                time_slot=time_slot
            )

        # Validate time order
        if start_time >= end_time:

            flash(
                "End time must be later than start time.",
                "danger"
            )

            return render_template(
                "admin/time_slots/edit.html",
                time_slot=time_slot
            )

        # Update
        time_slot.day = day
        time_slot.start_time = start_time
        time_slot.end_time = end_time

        db.session.commit()

        flash(
            "Time slot updated successfully.",
            "success"
        )

        return redirect(
            url_for("time_slots.index")
        )

    return render_template(
        "admin/time_slots/edit.html",
        time_slot=time_slot
    )


# =========================================================
# DELETE TIME SLOT
# =========================================================

@time_slots_bp.route(
    "/<int:time_slot_id>/delete",
    methods=["POST"]
)
@login_required
def delete(time_slot_id):

    time_slot = TimeSlot.query.get_or_404(
        time_slot_id
    )

    db.session.delete(time_slot)
    db.session.commit()

    flash(
        "Time slot deleted successfully.",
        "success"
    )

    return redirect(
        url_for("time_slots.index")
    )