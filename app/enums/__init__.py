from enum import Enum


class UserRole(Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"


class OrderStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class TransactionStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PENDING = "pending"
