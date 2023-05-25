from ..models import db, PaymentTransaction

print("payment service.py")

class PaymentService:
    @staticmethod
    def create_payment(data):
        payment = PaymentTransaction(**data)
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def get_payment(id):
        return PaymentTransaction.query.get(id)

    @staticmethod
    def update_payment(id, data):
        payment = PaymentTransaction.query.get(id)
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment

    @staticmethod
    def delete_payment(id):
        PaymentTransaction.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def get_payments():
        return PaymentTransaction.query.all()
