from .base_service import BaseService
from ..models import PaymentTransaction


class PaymentService(BaseService):
    model = PaymentTransaction
