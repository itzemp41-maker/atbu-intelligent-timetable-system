from app import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    code = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    units = db.Column(
        db.Integer,
        nullable=False
    )

    course_type = db.Column(
        db.String(30),
        nullable=False,
        default="Theory"
    )

    level_id = db.Column(
        db.Integer,
        db.ForeignKey("levels.id"),
        nullable=False
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    level = db.relationship(
        "Level",
        back_populates="courses"
    )

    timetable_entries = db.relationship(
        "Timetable",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    offerings = db.relationship(
        "CourseOffering",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Course {self.code}>"