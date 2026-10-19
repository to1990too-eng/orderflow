# order_service/schemas.py
from datetime import datetime

from pydantic import BaseModel

from order_service.models import OrderStatus


class OrderCreate(BaseModel):
    item_name: str
    price: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    item_name: str
    price: int
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}

class OrderStatusUpdate(BaseModel):
    status: OrderStatus = OrderStatus.PROCESSED