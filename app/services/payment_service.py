from . import db, PaymentTransaction


class PaymentService:
    @staticmethod
    def process_payment(self, order_id, payment_details):
        # Handle payment processing using a payment gateway or third-party service
        # Placeholder code for demonstration purposes
        payment_transaction = PaymentTransaction(
            order_id=order_id,
            transaction_id="123456",
            status="completed",
            amount=payment_details["amount"],
        )
        db.session.add(payment_transaction)
        db.session.commit()
        return payment_transaction

    @staticmethod
    def get_payment_status(self, order_id):
        # Get the status of a payment transaction
        payment_transaction = PaymentTransaction.query.filter_by(
            order_id=order_id
        ).first()
        if payment_transaction:
            return payment_transaction.status
        return None

    @staticmethod
    def refund_payment(self, order_id):
        # Handle refund requests and cancellations of payments
        payment_transaction = PaymentTransaction.query.filter_by(
            order_id=order_id
        ).first()
        if payment_transaction and payment_transaction.status == "completed":
            payment_transaction.status = "refunded"
            db.session.commit()
            return True
        return False
