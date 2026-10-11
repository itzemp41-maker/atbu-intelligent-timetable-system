from app import db


class Level(db.Model):

    __tablename__ = "levels"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )

    programme = db.relationship(
        "Programme",
        back_populates="levels"
    )

    courses = db.relationship(
        "Course",
        back_populates="level",
        lazy=True
    )

    timetable_entries = db.relationship(
        "Timetable",
        back_populates="level",
        cascade="all, delete-orphan"
    )

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="level",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Level {self.name}>"