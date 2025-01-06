from . import db


class ReceiptItem(db.Model):
    __tablename__ = 'receipt_items'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    receipt_id = db.Column(db.BigInteger, db.ForeignKey('receipts.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2))
    qty = db.Column(db.Integer)

    def __repr__(self):
        return f'<ReceiptItem {self.description}>'