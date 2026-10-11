from app import db


class CourseOffering(db.Model):

    __tablename__ = "course_offerings"

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

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    course = db.relationship(
        "Course",
        back_populates="offerings"
    )

    lecturer = db.relationship(
        "Lecturer",
        back_populates="course_offerings"
    )

    semester = db.relationship(
        "Semester",
        back_populates="course_offerings"
    )

    level = db.relationship(
        "Level",
        back_populates="course_offerings"
    )

    def __repr__(self):

        return (
            f"<CourseOffering "
            f"{self.course_id} - "
            f"{self.lecturer_id} - "
            f"{self.semester_id}>"
        )