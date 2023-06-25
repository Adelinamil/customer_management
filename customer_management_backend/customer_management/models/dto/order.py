from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from customer_management.models.dto import Customer, Product
from customer_management.models.enum.order import OrderStatus


@dataclass
class Order:
    id: int
    customer_id: UUID
    product_id: int
    quantity: int
    total_price: Decimal
    dt: datetime
    status: OrderStatus

    customer: Customer | None = None
    product: Product | None = None
