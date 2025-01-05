from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('customer_id', name='customers_pkey'),
        UniqueConstraint('email', name='customers_email_key'),
        {'schema': 'public'}
    )

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(15))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    orders: Mapped[List['Orders']] = relationship('Orders', back_populates='customer')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('product_id', name='products_pkey'),
        {'schema': 'public'}
    )

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]] = mapped_column(Text)
    stock_quantity: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 3), server_default=text('0.0'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    order_items: Mapped[List['OrderItems']] = relationship('OrderItems', back_populates='product')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['public.customers.customer_id'], name='orders_customer_id_fkey'),
        PrimaryKeyConstraint('order_id', name='orders_pkey'),
        {'schema': 'public'}
    )

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    shipping_address: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    order_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'pending'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    customer: Mapped['Customers'] = relationship('Customers', back_populates='orders')
    order_items: Mapped[List['OrderItems']] = relationship('OrderItems', back_populates='order')
    shipments: Mapped[List['Shipments']] = relationship('Shipments', back_populates='order')


class OrderItems(Base):
    __tablename__ = 'order_items'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.order_id'], ondelete='CASCADE', name='order_items_order_id_fkey'),
        ForeignKeyConstraint(['product_id'], ['public.products.product_id'], name='order_items_product_id_fkey'),
        PrimaryKeyConstraint('order_item_id', name='order_items_pkey'),
        {'schema': 'public'}
    )

    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    order_id: Mapped[Optional[int]] = mapped_column(Integer)
    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    order: Mapped['Orders'] = relationship('Orders', back_populates='order_items')
    product: Mapped['Products'] = relationship('Products', back_populates='order_items')


class Shipments(Base):
    __tablename__ = 'shipments'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.order_id'], name='shipments_order_id_fkey'),
        PrimaryKeyConstraint('shipment_id', name='shipments_pkey'),
        UniqueConstraint('tracking_number', name='shipments_tracking_number_key'),
        {'schema': 'public'}
    )

    shipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tracking_number: Mapped[str] = mapped_column(String(100))
    carrier: Mapped[str] = mapped_column(String(100))
    order_id: Mapped[Optional[int]] = mapped_column(Integer)
    shipment_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    estimated_delivery_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'in transit'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    order: Mapped['Orders'] = relationship('Orders', back_populates='shipments')
    tracking_events: Mapped[List['TrackingEvents']] = relationship('TrackingEvents', back_populates='shipment')


class TrackingEvents(Base):
    __tablename__ = 'tracking_events'
    __table_args__ = (
        ForeignKeyConstraint(['shipment_id'], ['public.shipments.shipment_id'], name='tracking_events_shipment_id_fkey'),
        PrimaryKeyConstraint('tracking_event_id', name='tracking_events_pkey'),
        {'schema': 'public'}
    )

    tracking_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location: Mapped[str] = mapped_column(String(255))
    event_description: Mapped[str] = mapped_column(Text)
    shipment_id: Mapped[Optional[int]] = mapped_column(Integer)
    event_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    shipment: Mapped['Shipments'] = relationship('Shipments', back_populates='tracking_events')
