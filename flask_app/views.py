"""Docstring for file."""
import datetime

from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request
from flask_app.app import app, db
from flask_app.models import PaymentModel, PaymentTypeModel, PostStatus
from flask_app.serializers import PaymentSchema, PaymentTypeSchema
from flask_app.validate_credit_card import validate

payment_type_schema = PaymentTypeSchema()
payment_schema = PaymentSchema()

my_app = Blueprint('my_app', __name__)


@app.route('/payment', methods=['GET'])
@swag_from("docs/getPaymentProcess.yml")
def get_process_payment():
    """Docstring for function."""
    payments = PaymentModel.query.all()
    results = [
        {
            "CreditCardNumber": pay.CreditCardNumber,
            "CardHolder": pay.CardHolder,
            "ExpirationDate": pay.ExpirationDate,
            "SecurityCode": pay.SecurityCode,
            "Amount": pay.Amount,
        } for pay in payments]

    return {"count": len(results), "payments": results}


@app.route('/payment/', methods=['POST'])
@swag_from("docs/processPayment.yml")
def process_payment():
    """Docstring for function."""
    if request.is_json:
        data = request.get_json()

        errors = payment_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        data['CreditCardNumber'] = data['CreditCardNumber'].replace('-', '')
        if not validate(data['CreditCardNumber']):
            return jsonify({"message": 'Credit Card Number Not Valid!'}), 400

        val = datetime.datetime.strptime(data['ExpirationDate'], '%Y-%m-%d')
        val = val.date()
        if val < datetime.datetime.now().date():
            return jsonify({"message": 'Expired Credit Card'}), 400

        payment_type_id = None
        if data['Amount'] >= 21 and data['Amount'] <= 500:
            pay = PaymentTypeModel.query.get(2)
            if pay.is_available:
                payment_type_id = 2
            else:
                payment_type_id = 1
        elif data['Amount'] > 500:
            payment_type_id = 3
        else:
            payment_type_id = 1

        if payment_type_id:
            num = PaymentModel.query.filter(
                PaymentModel.CreditCardNumber == data['CreditCardNumber']
            ).all()
            if not num:
                try:
                    data['SecurityCode']
                    new_payment = PaymentModel(
                        CreditCardNumber=data['CreditCardNumber'],
                        CardHolder=data['CardHolder'],
                        ExpirationDate=data['ExpirationDate'],
                        SecurityCode=data['SecurityCode'],
                        Amount=data['Amount'],
                        payment_type_id=payment_type_id
                    )
                except KeyError:
                    new_payment = PaymentModel(
                        CreditCardNumber=data['CreditCardNumber'],
                        CardHolder=data['CardHolder'],
                        ExpirationDate=data['ExpirationDate'],
                        Amount=data['Amount'],
                        payment_type_id=payment_type_id
                    )
                db.session.add(new_payment)
                db.session.commit()
                return jsonify(new_payment.serialize()), 201
            else:
                pay = num[0]
                if pay.status.value != PostStatus.REJECT.value:
                    if pay.Amount > 500:
                        if pay.numberTrials <= 3:
                            pay.numberTrials = pay.numberTrials + 1
                            db.session.commit()
                        else:
                            pay.status = PostStatus.REJECT.value
                            db.session.commit()
                        return jsonify(pay.serialize()), 201
                    else:
                        return {
                            "message": "This payment is to be processed "
                        }, 400
                else:
                    return {"message": "This payment is Rejected"}, 400
        else:
            return {
                "message": "No payment type available for this Amount"
            }, 400
    else:
        return {"message": "The request payload is not in JSON format"}, 400


@app.route('/payment/type', methods=['GET'])
@swag_from("docs/get_payment_type.yml")
def get_payment_type():
    """Docstring for function."""
    payments_type = PaymentTypeModel.query.all()
    results = [
        {
            "name": pay.name,
            "value": pay.value,
            "is_available": pay.is_available
        } for pay in payments_type]

    return {"count": len(results), "payments_type": results}


@app.route('/payment/type/', methods=['POST'])
@swag_from("docs/payment_type.yml")
def payment_type():
    """Docstring for function."""
    if request.is_json:
        data = request.get_json()
        errors = payment_type_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        num = PaymentTypeModel.query.filter(
            PaymentTypeModel.name == data['name']).all()
        if num:
            return jsonify(
                {"message": 'A payment type with this name already exists'}
            ), 409
        try:
            data['is_available']
            new_payment_type = PaymentTypeModel(
                name=data['name'],
                value=data['value'],
                is_available=data['is_available']
            )
        except KeyError:
            new_payment_type = PaymentTypeModel(
                name=data['name'],
                value=data['value']
            )
        db.session.add(new_payment_type)
        db.session.commit()
        # print(new_payment.serialize(), file=sys.stdout)
        return jsonify(new_payment_type.serialize()), 201
    else:
        return {"error": "The request payload is not in JSON format"}


@app.route('/payment/type/<int:pk>', methods=['PUT'])
@swag_from("docs/payment_type_modified.yml")
def payment_type_modified(pk):
    """Docstring for function."""
    if request.is_json:
        data = request.get_json()
        errors = payment_type_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        num = PaymentTypeModel.query.filter(
            PaymentTypeModel.name == data['name'], PaymentTypeModel.id != pk
        ).all()
        if num:
            return jsonify(
                {"message": 'A payment type with this name already exists'}
            ), 409
        payment_type = PaymentTypeModel.query.get(pk)
        try:
            payment_type.name = data['name']
            payment_type.value = data['value']
            payment_type.is_available = data['is_available']
        except KeyError:
            payment_type.name = data['name']
            payment_type.value = data['value']

        db.session.commit()
        return jsonify(payment_type.serialize()), 201
    else:
        return {"error": "The request payload is not in JSON format"}

if __name__ == '__main__':
    app.run(debug=True)
