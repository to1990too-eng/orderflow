# order_service/api/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.database import get_db
from order_service.models import Order, OrderStatus
from order_service.rabbit import publish_order_created
from order_service.schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from order_service.security import get_current_user_id

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    payload: OrderCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    order = Order(
        user_id=user_id,
        item_name=payload.item_name,
        price=payload.price,
        status=OrderStatus.PENDING,
    )
    db.add(order)
    await db.flush()
    await db.refresh(order)

    # Публикуем событие в RabbitMQ (на Шаге 4)
    await publish_order_created(order.id, user_id, payload.item_name)

    return order

@router.get("", response_model=list[OrderResponse])
async def list_orders(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    )
    return result.scalars().all()

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Внутренний эндпоинт — без JWT-защиты (вызывается notification_service)
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = payload.status
    await db.flush()
    await db.refresh(order)
    return order