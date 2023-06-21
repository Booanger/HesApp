from . import db, Table
import qrcode
from io import BytesIO
import base64
import json


class QRCodeService:
    @staticmethod
    def get_table_id_and_restaurant_id(table_id):
        table = Table.query.filter_by(id=table_id, is_active=True).first()
        if table:
            return {"restaurant_id": table.restaurant_id, "table_id": table.id}, 200
        return {"msg": "Table not found"}, 404

    @staticmethod
    def generate_qr_codes_for_restaurant(restaurant_id: int):
        # Retrieve the table_ids associated with the restaurant_id
        table_ids = (
            Table.query.filter_by(restaurant_id=restaurant_id, is_active=True)
            .with_entities(Table.id)
            .all()
        )

        qr_codes = []
        for table_tuple in table_ids:
            table_id = table_tuple[0]
            # Generate the QR code data (e.g., restaurant_id and table_id)
            qr_data = {"restaurant_id": restaurant_id, "table_id": table_id}

            # Convert the data to a JSON string with double quotes
            qr_data_str = json.dumps(qr_data)

            # Create a QR code from the data
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data_str)
            qr.make(fit=True)

            img = qr.make_image(fill="black", back_color="white")

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            qr_codes.append((img_str, table_id))

        return qr_codes


""" Might be useful:
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
"""
