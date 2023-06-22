import os
import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.services import UserService, User, UserRole
import time


class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["FLASK_ENV"] = "testing"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_customer_not_found(self):
        # Act
        response, status_code = UserService.get_customer(1)

        # Assert
        self.assertEqual(status_code, 404)
        self.assertIn("msg", response)

    def test_get_customer_found(self):
        # Arrange
        # Create a customer user in the database
        customer = User(
            username="testuser",
            email="test@example.com",
            password="password",
            phone="1234567890",
            role=UserRole.CUSTOMER,
        )
        db.session.add(customer)
        db.session.commit()

        # Act
        response, status_code = UserService.get_customer(customer.id)

        # Assert
        self.assertEqual(status_code, 200)

    def test_register_customer_existing_user(self):
        # Arrange
        # Create an existing user in the database
        existing_user = User(
            username="testuser",
            email="test@example.com",
            password="password",
            phone="1234567890",
        )
        db.session.add(existing_user)
        db.session.commit()

        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "phone": "1234567890",
        }

        # Act
        response, status_code = UserService.register_customer(**data)

        # Assert
        self.assertEqual(status_code, 409)
        self.assertIn("error", response)


if __name__ == "__main__":
    unittest.main()
