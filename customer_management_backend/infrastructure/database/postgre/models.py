from __future__ import annotations
import uuid
from decimal import Decimal

from datetime import datetime

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import String, Enum, DateTime, func, Integer, Text, BigInteger, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID

from customer_management.models import dto
from customer_management.models.enum.order import OrderStatus
from customer_management.models.enum.user import UserType
from customer_management.models.interfaces.dto import DTOProtocol


class Base(DeclarativeBase):
    def to_dto(self) -> DTOProtocol:
        raise NotImplementedError

    @classmethod
    def from_dto(cls, dto_object: DTOProtocol):
        raise NotImplementedError


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    second_name: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_activity: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def to_dto(self) -> dto.User:
        return dto.User(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            second_name=self.second_name,
            user_type=self.user_type,
            created=self.created,
            last_activity=self.last_activity
        )

    @classmethod
    def from_dto(cls, user_dto: dto.UserWithPassword) -> User:
        return User(
            id=user_dto.id,
            username=user_dto.username,
            first_name=user_dto.first_name,
            second_name=user_dto.second_name,
            user_type=user_dto.user_type,
            password=user_dto.hashed_password
        )


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    second_name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def to_dto(self) -> dto.Customer:
        return dto.Customer(
            id=self.id,
            first_name=self.first_name,
            second_name=self.second_name,
            address=self.address,
            phone_number=self.phone_number,
            created=self.created
        )

    @classmethod
    def from_dto(cls, customer_dto: dto.Customer) -> Customer:
        return Customer(
            id=customer_dto.id,
            first_name=customer_dto.first_name,
            second_name=customer_dto.second_name,
            address=customer_dto.address,
            phone_number=customer_dto.phone_number
        )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(String, nullable=True)
    in_stock: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_location: Mapped[str] = mapped_column(String, nullable=True)

    def to_dto(self) -> dto.Product:
        return dto.Product(
            id=self.id,
            title=self.title,
            brand=self.brand,
            category=self.category,
            color=self.color,
            size=self.size,
            in_stock=self.in_stock,
            description=self.description,
            image_location=self.image_location
        )


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('customers.id', ondelete='CASCADE'),
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    dt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)

    customer: Mapped['Customer'] = relationship()
    product: Mapped['Product'] = relationship()

    def to_dto(self, with_customer: bool = True, with_product: bool = True) -> dto.Order:
        return dto.Order(
            id=self.id,
            customer_id=self.customer_id,
            product_id=self.product_id,
            quantity=self.quantity,
            total_price=self.total_price,
            dt=self.dt,
            status=self.status,
            customer=self.customer.to_dto() if with_customer else None,
            product=self.product.to_dto() if with_product else None
        )
