from . import db, Table


class QRCodeService:
    @staticmethod
    def generate_qr_code(data):
        # Generate a QR code based on the provided data
        # Placeholder code for demonstration purposes
        qr_code = f"QR Code for: {data}"
        return qr_code

    @staticmethod
    def validate_qr_code(qr_code):
        # Validate the scanned QR code to ensure it corresponds to a valid table or order
        # Placeholder code for demonstration purposes
        return True

    @staticmethod
    def assign_table(qr_code, customer_id):
        # Assign a table to a customer based on the scanned QR code
        # Placeholder code for demonstration purposes
        table_id = int(qr_code.split(":")[1])
        table = Table.query.get(table_id)
        if table:
            table.customer_id = customer_id
            db.session.commit()
            return table
        return None
