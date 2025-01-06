from . import db


class Receipt(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    merchant_name = db.Column(db.String(255))
    merchant_address = db.Column(db.Text)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    total = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10))
    ocr_confidence = db.Column(db.Numeric(5, 2))

    # Relationships
    items = db.relationship('ReceiptItem', backref='receipt', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Receipt {self.merchant_name}>'