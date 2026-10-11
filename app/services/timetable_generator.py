import random

from app import db

from app.models import (
    Timetable,
    CourseOffering,
    Venue,
    TimeSlot
)


class TimetableGenerator:

    def __init__(self):

        self.conflicts = []
        self.generated = 0

        # =================================================
        # UNIVERSITY TEACHING DAYS
        # =================================================

        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]

        # =================================================
        # ALLOWED TEACHING PERIODS
        #
        # 1:00 PM - 2:00 PM is NOT included because it is
        # reserved for prayer.
        # =================================================

        self.allowed_periods = [
            ("09:00", "11:00"),
            ("11:00", "13:00"),
            ("14:00", "16:00"),
            ("16:00", "17:00")
        ]

        # =================================================
        # DAY ORDER
        # =================================================

        self.day_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5
        }

    # =====================================================
    # MAIN GENERATION METHOD
    # =====================================================

    def generate(self):

        self.conflicts = []
        self.generated = 0

        # =================================================
        # REMOVE PREVIOUS TIMETABLE
        # =================================================

        try:

            Timetable.query.delete()

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            return {
                "success": False,
                "message": (
                    "Could not clear the previous timetable: "
                    f"{error}"
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # LOAD COURSE OFFERINGS
        # =================================================

        offerings = (
            CourseOffering.query
            .join(CourseOffering.course)
            .all()
        )

        if not offerings:

            return {
                "success": False,
                "message": (
                    "No course offerings are available. "
                    "Add course offerings before generating."
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # RANDOMIZE COURSE ORDER
        #
        # This prevents the same courses from always being
        # assigned first.
        # =================================================

        random.shuffle(offerings)

        # =================================================
        # LOAD VENUES
        # =================================================

        venues = (
            Venue.query
            .order_by(
                Venue.capacity.desc()
            )
            .all()
        )

        if not venues:

            return {
                "success": False,
                "message": (
                    "No venues are available. "
                    "Add venues before generating."
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # LOAD TIME SLOTS
        # =================================================

        all_time_slots = (
            TimeSlot.query
            .filter(
                TimeSlot.day.in_(self.days)
            )
            .all()
        )

        # =================================================
        # FILTER ONLY THE FOUR APPROVED PERIODS
        # =================================================

        valid_time_slots = []

        for slot in all_time_slots:

            if not slot.start_time or not slot.end_time:
                continue

            start = slot.start_time.strftime("%H:%M")
            end = slot.end_time.strftime("%H:%M")

            if (start, end) in self.allowed_periods:

                valid_time_slots.append(slot)

        # =================================================
        # CHECK VALID TIME SLOTS
        # =================================================

        if not valid_time_slots:

            return {
                "success": False,
                "message": (
                    "No valid timetable periods were found. "
                    "Create these periods: "
                    "9:00-11:00, 11:00-13:00, "
                    "14:00-16:00 and 16:00-17:00."
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # IMPORTANT:
        #
        # Any 1:00 PM - 2:00 PM slot is automatically
        # excluded because it is not in allowed_periods.
        # =================================================

        # =================================================
        # GROUP SLOTS BY DAY
        # =================================================

        slots_by_day = {
            day: []
            for day in self.days
        }

        for slot in valid_time_slots:

            if slot.day in slots_by_day:

                slots_by_day[slot.day].append(slot)

        # =================================================
        # AVAILABLE DAYS
        # =================================================

        available_days = [
            day
            for day in self.days
            if slots_by_day[day]
        ]

        if not available_days:

            return {
                "success": False,
                "message": (
                    "No valid Monday-Friday timetable "
                    "periods were found."
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # RESOURCE TRACKING
        # =================================================

        lecturer_slots = set()

        venue_slots = set()

        student_group_slots = set()

        # =================================================
        # DAY LOAD
        # =================================================

        day_load = {
            day: 0
            for day in available_days
        }

        # =================================================
        # SLOT LOAD
        # =================================================

        slot_load = {
            slot.id: 0
            for slot in valid_time_slots
        }

        # =================================================
        # GENERATE COURSES
        # =================================================

        for offering in offerings:

            assigned = self._assign_offering(
                offering=offering,
                venues=venues,
                slots_by_day=slots_by_day,
                lecturer_slots=lecturer_slots,
                venue_slots=venue_slots,
                student_group_slots=student_group_slots,
                day_load=day_load,
                slot_load=slot_load
            )

            if assigned:

                self.generated += 1

            else:

                if offering.course:

                    course_name = offering.course.code

                else:

                    course_name = (
                        f"Course #{offering.course_id}"
                    )

                self.conflicts.append(
                    f"Could not schedule {course_name} "
                    f"for Level {offering.level_id}, "
                    f"Semester {offering.semester_id}."
                )

        # =================================================
        # SAVE
        # =================================================

        try:

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            return {
                "success": False,
                "message": (
                    "An error occurred while saving "
                    f"the timetable: {error}"
                ),
                "generated": 0,
                "conflicts": []
            }

        # =================================================
        # NOTHING GENERATED
        # =================================================

        if self.generated == 0:

            return {
                "success": False,
                "message": (
                    "No timetable entries could be generated."
                ),
                "generated": 0,
                "conflicts": self.conflicts
            }

        # =================================================
        # PARTIAL GENERATION
        # =================================================

        if self.conflicts:

            return {
                "success": True,
                "message": (
                    "Timetable generated with some "
                    "unscheduled courses."
                ),
                "generated": self.generated,
                "conflicts": self.conflicts
            }

        # =================================================
        # COMPLETE GENERATION
        # =================================================

        return {
            "success": True,
            "message": (
                "Timetable generated successfully "
                "from Monday to Friday."
            ),
            "generated": self.generated,
            "conflicts": []
        }

    # =====================================================
    # ASSIGN COURSE
    # =====================================================

    def _assign_offering(
        self,
        offering,
        venues,
        slots_by_day,
        lecturer_slots,
        venue_slots,
        student_group_slots,
        day_load,
        slot_load
    ):

        # =================================================
        # CREATE ALL POSSIBLE COMBINATIONS
        #
        # Example:
        #
        # Monday    9-11
        # Monday    11-1
        # Monday    2-4
        # Monday    4-5
        # Tuesday   9-11
        # ...
        # Friday    4-5
        # =================================================

        candidates = []

        for day in slots_by_day:

            for time_slot in slots_by_day[day]:

                candidates.append(
                    (
                        day,
                        time_slot
                    )
                )

        # =================================================
        # RANDOMIZE THE CANDIDATES
        #
        # This is the major change.
        #
        # The generator no longer always starts with:
        #
        # Monday 9-11
        #
        # Instead, it randomly selects among the valid
        # Monday-Friday periods.
        # =================================================

        random.shuffle(candidates)

        # =================================================
        # TRY RANDOMIZED CANDIDATES
        # =================================================

        for day, time_slot in candidates:

            # =================================================
            # LECTURER CONFLICT
            # =================================================

            if offering.lecturer_id is not None:

                lecturer_key = (
                    offering.lecturer_id,
                    time_slot.id
                )

                if lecturer_key in lecturer_slots:

                    continue

            else:

                lecturer_key = None

            # =================================================
            # STUDENT GROUP CONFLICT
            #
            # Same level + semester cannot have two courses
            # during the same period.
            # =================================================

            student_group_key = (
                offering.level_id,
                offering.semester_id,
                time_slot.id
            )

            if student_group_key in student_group_slots:

                continue

            # =================================================
            # FIND AVAILABLE VENUE
            # =================================================

            venue = self._find_venue(
                offering=offering,
                time_slot=time_slot,
                venues=venues,
                venue_slots=venue_slots
            )

            if venue is None:

                continue

            # =================================================
            # CREATE TIMETABLE ENTRY
            # =================================================

            entry = Timetable(

                course_id=offering.course_id,

                lecturer_id=offering.lecturer_id,

                venue_id=venue.id,

                time_slot_id=time_slot.id,

                semester_id=offering.semester_id,

                level_id=offering.level_id,

                # Always use the day belonging to the
                # selected TimeSlot.
                day=time_slot.day
            )

            db.session.add(entry)

            # =================================================
            # RECORD LECTURER
            # =================================================

            if lecturer_key is not None:

                lecturer_slots.add(
                    lecturer_key
                )

            # =================================================
            # RECORD VENUE
            # =================================================

            venue_slots.add(
                (
                    venue.id,
                    time_slot.id
                )
            )

            # =================================================
            # RECORD STUDENT GROUP
            # =================================================

            student_group_slots.add(
                student_group_key
            )

            # =================================================
            # UPDATE LOADS
            # =================================================

            day_load[day] += 1

            slot_load[time_slot.id] += 1

            return True

        return False

    # =====================================================
    # FIND SUITABLE VENUE
    # =====================================================

    def _find_venue(
        self,
        offering,
        time_slot,
        venues,
        venue_slots
    ):

        course = offering.course

        # =================================================
        # RANDOMIZE VENUE ORDER
        #
        # This also prevents every course from always
        # receiving the same venue.
        # =================================================

        available_venues = list(venues)

        random.shuffle(available_venues)

        # =================================================
        # FIND VENUE
        # =================================================

        for venue in available_venues:

            venue_key = (
                venue.id,
                time_slot.id
            )

            # =================================================
            # VENUE OCCUPIED
            # =================================================

            if venue_key in venue_slots:

                continue

            # =================================================
            # COURSE TYPE
            # =================================================

            course_type = ""

            if course and course.course_type:

                course_type = (
                    course.course_type
                    .strip()
                    .lower()
                )

            # =================================================
            # VENUE TYPE
            # =================================================

            venue_type = ""

            if venue.venue_type:

                venue_type = (
                    venue.venue_type
                    .strip()
                    .lower()
                )

            # =================================================
            # PRACTICAL COURSE
            # =================================================

            if course_type == "practical":

                if "lab" not in venue_type:

                    continue

            # =================================================
            # VENUE ACCEPTED
            # =================================================

            return venue

        return None