"""Docstring for file."""
from marshmallow import Schema, fields
from marshmallow.validate import Length


class PaymentSchema(Schema):
    """Docstring for class."""

    CreditCardNumber = fields.Str(
        required=True, validate=Length(max=255), allow_none=False)
    CardHolder = fields.Str(
        required=True, validate=Length(max=255), allow_none=False)
    ExpirationDate = fields.Date(required=True)
    SecurityCode = fields.Str(
        required=False, validate=Length(min=3, max=3), allow_none=True)
    Amount = fields.Float(required=True)
    numberTrials = fields.Int(required=False)

    class Meta:
        """Docstring for class."""

        strict = True
        fields = ('id', 'CreditCardNumber', 'CardHolder',
                  'SecurityCode', 'ExpirationDate', 'Amount')


class PaymentTypeSchema(Schema):
    """Docstring for class."""

    name = fields.Str(required=True, validate=Length(max=20), allow_none=False)
    value = fields.Str(
        required=True, validate=Length(max=100), allow_none=False)
    is_available = fields.Boolean(required=False)

    class Meta:
        """Docstring for class."""

        strict = True
        fields = ('id', 'name', 'value', 'is_available')
