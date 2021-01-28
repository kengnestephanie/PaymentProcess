"""Docstring for file."""
import enum

from flask_app.app import db


class PaymentTypeModel(db.Model):
    """Docstring for class."""

    __tablename__ = 'paymentType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    is_available = db.Column(db.Boolean(), nullable=True, default=True)

    def __repr__(self):
        """Docstring for function."""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """Docstring for function."""
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'is_available': self.is_available
        }


class PostStatus(enum.Enum):
    REJECT = 'Reject'
    TO_TREAT = 'To Treat'


class PaymentModel(db.Model):
    """Docstring for class."""

    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    CreditCardNumber = db.Column(db.String(255), nullable=False)
    CardHolder = db.Column(db.String(255), nullable=False)
    ExpirationDate = db.Column(db.Date(), nullable=False)
    SecurityCode = db.Column(db.String(3), nullable=True)
    Amount = db.Column(db.Float(), nullable=False)
    numberTrials = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(
        db.Enum(PostStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=PostStatus.TO_TREAT.value,
        server_default=PostStatus.TO_TREAT.value
    )
    payment_type_id = db.Column(db.Integer, db.ForeignKey('paymentType.id'))
    payment_type = db.relationship(
        "PaymentTypeModel", backref=db.backref("paymentType", uselist=False))

    def __repr__(self):
        """Docstring for function."""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """Docstring for function."""
        return {
            'id': self.id,
            'CreditCardNumber': self.CreditCardNumber,
            'CardHolder': self.CardHolder,
            'ExpirationDate': self.ExpirationDate,
            'SecurityCode': self.SecurityCode,
            'Amount': self.Amount,
            "numberTrials": self.numberTrials,
            'payment_type': self.payment_type.value,
            'status': self.status.value
        }
