from app import db


class Timetable(db.Model):

    __tablename__ = "timetables"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    lecturer_id = db.Column(
        db.Integer,
        db.ForeignKey("lecturers.id"),
        nullable=False
    )

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venues.id"),
        nullable=False
    )

    time_slot_id = db.Column(
        db.Integer,
        db.ForeignKey("time_slots.id"),
        nullable=False
    )

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semesters.id"),
        nullable=False
    )

    level_id = db.Column(
        db.Integer,
        db.ForeignKey("levels.id"),
        nullable=False
    )

    day = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    course = db.relationship(
        "Course",
        back_populates="timetable_entries"
    )

    lecturer = db.relationship(
        "Lecturer",
        back_populates="timetable_entries"
    )

    venue = db.relationship(
        "Venue",
        back_populates="timetable_entries"
    )

    time_slot = db.relationship(
        "TimeSlot",
        back_populates="timetable_entries"
    )

    semester = db.relationship(
        "Semester",
        back_populates="timetable_entries"
    )

    level = db.relationship(
        "Level",
        back_populates="timetable_entries"
    )

    def __repr__(self):
        return f"<Timetable {self.course_id} - {self.day}>"