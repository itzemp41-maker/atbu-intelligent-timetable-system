from app import db


class Semester(db.Model):

    __tablename__ = "semesters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    timetable_entries = db.relationship(
        "Timetable",
        back_populates="semester",
        cascade="all, delete-orphan"
    )

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="semester",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Semester {self.name}>"