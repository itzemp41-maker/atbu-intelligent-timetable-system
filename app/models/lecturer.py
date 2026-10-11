from app import db


class Lecturer(db.Model):

    __tablename__ = "lecturers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    staff_id = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship(
        "Department",
        back_populates="lecturers"
    )

    timetable_entries = db.relationship(
        "Timetable",
        back_populates="lecturer",
        cascade="all, delete-orphan"
    )

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="lecturer",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Lecturer {self.name}>"