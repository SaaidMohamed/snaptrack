from . import db
import datetime


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(50))

    # Relationships
    receipts = db.relationship('Receipt', backref='user', cascade="all, delete-orphan")
    receipt_items = db.relationship('ReceiptItem', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.user_name}>'