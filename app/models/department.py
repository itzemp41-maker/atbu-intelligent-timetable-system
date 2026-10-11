from app import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    code = db.Column(
        db.String(20),
        nullable=True,
        unique=True
    )

    programmes = db.relationship(
        "Programme",
        back_populates="department",
        lazy=True
    )

    lecturers = db.relationship(
        "Lecturer",
        back_populates="department",
        lazy=True
    )

    def __repr__(self):
        return f"<Department {self.name}>"