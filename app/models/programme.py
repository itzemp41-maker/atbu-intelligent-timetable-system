from app import db


class Programme(db.Model):
    __tablename__ = "programmes"

    id = db.Column(
        db.Integer,
        primary_key=True
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
        back_populates="programmes"
    )

    levels = db.relationship(
        "Level",
        back_populates="programme",
        lazy=True
    )

    def __repr__(self):
        return f"<Programme {self.name}>"