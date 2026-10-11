from app import db


class TimeSlot(db.Model):

    __tablename__ = "time_slots"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    day = db.Column(
        db.String(20),
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    timetable_entries = db.relationship(
        "Timetable",
        back_populates="time_slot",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<TimeSlot "
            f"{self.day} "
            f"{self.start_time}-"
            f"{self.end_time}>"
        )