from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="admin"
    )

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash == password

    def __repr__(self):
        return f"<User {self.username}>"