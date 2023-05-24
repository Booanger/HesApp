from enum import Enum

print("enums __init__.py")

class UserRole(Enum):
    CUSTOMER = 'customer'
    STAFF = 'staff'
    ADMIN = 'admin'
    
class OrderStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    PREPARING = 'preparing'
    READY = 'ready'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

class TransactionStatus(Enum):
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    PENDING = 'pending'