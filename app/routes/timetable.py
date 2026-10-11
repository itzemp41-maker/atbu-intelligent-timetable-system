from collections import OrderedDict

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from app import db

from app.models import (
    Timetable,
    CourseOffering,
    Venue,
    TimeSlot,
    Lecturer,
    Level,
    Semester
)

from app.services.timetable_generator import TimetableGenerator


# =========================================================
# TIMETABLE BLUEPRINT
# =========================================================

timetable_bp = Blueprint(
    "timetable",
    __name__,
    url_prefix="/timetable"
)


# =========================================================
# OFFICIAL ACADEMIC WEEK
# =========================================================

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]


# =========================================================
# OFFICIAL TEACHING PERIODS
#
# 09:00 AM - 11:00 AM
# 11:00 AM - 01:00 PM
# 02:00 PM - 04:00 PM
# 04:00 PM - 05:00 PM
#
# 01:00 PM - 02:00 PM is excluded for prayer.
# =========================================================

ALLOWED_PERIODS = [
    ("09:00", "11:00"),
    ("11:00", "13:00"),
    ("14:00", "16:00"),
    ("16:00", "17:00")
]


# =========================================================
# VIEW TIMETABLE
# =========================================================

@timetable_bp.route("/")
@login_required
def index():

    # =====================================================
    # GET FILTER VALUES
    # =====================================================

    selected_level_id = request.args.get(
        "level_id",
        type=int
    )

    selected_semester_id = request.args.get(
        "semester_id",
        type=int
    )

    # =====================================================
    # LOAD LEVELS
    # =====================================================

    levels = (
        Level.query
        .order_by(
            Level.name.asc()
        )
        .all()
    )

    # =====================================================
    # LOAD SEMESTERS
    # =====================================================

    semesters = (
        Semester.query
        .order_by(
            Semester.name.asc()
        )
        .all()
    )

    # =====================================================
    # LOAD TIMETABLE ENTRIES
    # =====================================================

    query = Timetable.query

    # =====================================================
    # APPLY LEVEL FILTER
    # =====================================================

    if selected_level_id:

        query = query.filter(
            Timetable.level_id == selected_level_id
        )

    # =====================================================
    # APPLY SEMESTER FILTER
    # =====================================================

    if selected_semester_id:

        query = query.filter(
            Timetable.semester_id == selected_semester_id
        )

    # =====================================================
    # GET ENTRIES
    # =====================================================

    entries = query.all()

    # =====================================================
    # DAY ORDER
    # =====================================================

    day_order = {
        day.lower(): index
        for index, day in enumerate(DAYS)
    }

    # =====================================================
    # SORT ENTRIES
    # =====================================================

    entries.sort(
        key=lambda entry: (
            day_order.get(
                (entry.day or "").strip().lower(),
                99
            ),

            entry.time_slot.start_time
            if entry.time_slot
            else None,

            entry.level.name.lower()
            if entry.level
            else "",

            entry.course.code.lower()
            if entry.course
            else ""
        )
    )

    # =====================================================
    # LOAD MONDAY-FRIDAY TIME SLOTS
    # =====================================================

    weekday_slots = (
        TimeSlot.query
        .filter(
            TimeSlot.day.in_(DAYS)
        )
        .all()
    )

    # =====================================================
    # CREATE UNIQUE PERIODS
    #
    # We use the same time periods across all five days.
    # =====================================================

    unique_periods = OrderedDict()

    for slot in weekday_slots:

        if not slot.start_time or not slot.end_time:
            continue

        period_key = (
            slot.start_time,
            slot.end_time
        )

        if period_key not in unique_periods:

            unique_periods[period_key] = {
                "start_time": slot.start_time,
                "end_time": slot.end_time
            }

    # =====================================================
    # SORT PERIODS
    # =====================================================

    periods = sorted(
        unique_periods.values(),
        key=lambda period: (
            period["start_time"],
            period["end_time"]
        )
    )

    # =====================================================
    # BUILD TIMETABLE GRID
    #
    # DAY = ROW
    # TIME = COLUMN
    # =====================================================

    timetable_grid = OrderedDict()

    for day in DAYS:

        timetable_grid[day] = OrderedDict()

        for period in periods:

            matching_entries = []

            for entry in entries:

                # -------------------------------------------------
                # CHECK DAY
                # -------------------------------------------------

                entry_day = (
                    entry.day or ""
                ).strip().lower()

                if entry_day != day.lower():
                    continue

                # -------------------------------------------------
                # CHECK TIME SLOT
                # -------------------------------------------------

                if not entry.time_slot:
                    continue

                entry_start = entry.time_slot.start_time
                entry_end = entry.time_slot.end_time

                if (
                    entry_start == period["start_time"]
                    and
                    entry_end == period["end_time"]
                ):

                    matching_entries.append(entry)

            # -------------------------------------------------
            # SORT COURSES INSIDE CELL
            # -------------------------------------------------

            matching_entries.sort(
                key=lambda entry: (
                    entry.level.name.lower()
                    if entry.level
                    else "",

                    entry.course.code.lower()
                    if entry.course
                    else ""
                )
            )

            period_key = (
                period["start_time"],
                period["end_time"]
            )

            timetable_grid[day][period_key] = (
                matching_entries
            )

    # =====================================================
    # SUMMARY
    # =====================================================

    unique_courses = {
        entry.course_id
        for entry in entries
    }

    active_days = {
        (entry.day or "").strip().lower()
        for entry in entries
    }

    active_day_count = sum(
        1
        for day in DAYS
        if day.lower() in active_days
    )

    # =====================================================
    # SELECTED LEVEL NAME
    # =====================================================

    selected_level = None

    if selected_level_id:

        selected_level = next(
            (
                level
                for level in levels
                if level.id == selected_level_id
            ),
            None
        )

    # =====================================================
    # SELECTED SEMESTER NAME
    # =====================================================

    selected_semester = None

    if selected_semester_id:

        selected_semester = next(
            (
                semester
                for semester in semesters
                if semester.id == selected_semester_id
            ),
            None
        )

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "timetable/index.html",

        timetable_entries=entries,

        timetable_grid=timetable_grid,

        days=DAYS,

        periods=periods,

        levels=levels,

        semesters=semesters,

        selected_level_id=selected_level_id,

        selected_semester_id=selected_semester_id,

        selected_level=selected_level,

        selected_semester=selected_semester,

        total_courses=len(unique_courses),

        total_time_slots=len(periods),

        total_days=active_day_count
    )


# =========================================================
# GENERATE TIMETABLE
# =========================================================

@timetable_bp.route(
    "/generate",
    methods=["GET", "POST"]
)
@login_required
def generate():

    # =====================================================
    # GET REQUEST
    # =====================================================

    if request.method == "GET":

        resource_counts = {

            "courses":
                CourseOffering.query.count(),

            "lecturers":
                Lecturer.query.count(),

            "venues":
                Venue.query.count(),

            "time_slots":
                TimeSlot.query.count(),

            "levels":
                Level.query.count(),

            "semesters":
                Semester.query.count()
        }

        return render_template(
            "timetable/generate.html",
            resource_counts=resource_counts
        )

    # =====================================================
    # POST REQUEST
    # =====================================================

    try:

        courses_count = CourseOffering.query.count()

        lecturers_count = Lecturer.query.count()

        venues_count = Venue.query.count()

        time_slots_count = TimeSlot.query.count()

        levels_count = Level.query.count()

        semesters_count = Semester.query.count()

        # =================================================
        # VALIDATE RESOURCES
        # =================================================

        if courses_count == 0:

            flash(
                "Cannot generate timetable because there are no course offerings.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        if lecturers_count == 0:

            flash(
                "Cannot generate timetable because there are no lecturers.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        if venues_count == 0:

            flash(
                "Cannot generate timetable because there are no venues.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        if time_slots_count == 0:

            flash(
                "Cannot generate timetable because there are no time slots.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        if levels_count == 0:

            flash(
                "Cannot generate timetable because there are no academic levels.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        if semesters_count == 0:

            flash(
                "Cannot generate timetable because there are no semesters.",
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        # =================================================
        # CLEAR OLD TIMETABLE
        # =================================================

        Timetable.query.delete()

        db.session.commit()

        # =================================================
        # RUN GENERATOR
        # =================================================

        generator = TimetableGenerator()

        result = generator.generate()

        # =================================================
        # CHECK RESULT
        # =================================================

        if not result.get("success"):

            flash(
                result.get(
                    "message",
                    "Timetable generation failed."
                ),
                "danger"
            )

            return redirect(
                url_for("timetable.generate")
            )

        generated = result.get(
            "generated",
            0
        )

        conflicts = result.get(
            "conflicts",
            []
        )

        # =================================================
        # DISPLAY RESULT
        # =================================================

        if conflicts:

            flash(
                f"Timetable generated successfully with "
                f"{generated} scheduled course(s), but "
                f"{len(conflicts)} course(s) could not be scheduled.",
                "warning"
            )

            for conflict in conflicts[:5]:

                flash(
                    conflict,
                    "warning"
                )

        else:

            flash(
                f"Timetable generated successfully. "
                f"{generated} course(s) scheduled.",
                "success"
            )

        return redirect(
            url_for("timetable.index")
        )

    except Exception as error:

        db.session.rollback()

        print(
            "TIMETABLE GENERATION ERROR:",
            error
        )

        flash(
            "An unexpected error occurred while generating "
            "the timetable. Check the terminal for details.",
            "danger"
        )

        return redirect(
            url_for("timetable.generate")
        )


# =========================================================
# CLEAR TIMETABLE
# =========================================================

@timetable_bp.route(
    "/clear",
    methods=["POST"]
)
@login_required
def clear():

    try:

        Timetable.query.delete()

        db.session.commit()

        flash(
            "Timetable cleared successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        print(
            "TIMETABLE CLEAR ERROR:",
            error
        )

        flash(
            "Unable to clear the timetable.",
            "danger"
        )

    return redirect(
        url_for("timetable.index")
    )