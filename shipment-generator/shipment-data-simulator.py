import random
from datetime import datetime, date, timedelta
import logging
import sys

from faker import Factory
import faker
import faker_commerce

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models_public import Customers, Products, Orders, OrderItems, Shipments, TrackingEvents
import signal

def handle_sigterm(*args):
    raise KeyboardInterrupt()

logging.basicConfig(stream=sys.stdout)
logging.getLogger().setLevel(logging.INFO)

engine = create_engine('postgresql://delivery_user:delivery_pass@postgres-local:5432/microservices-delivery')
Base = declarative_base()

def create_customer():
    return Customers(
        first_name= faker.random_choices(elements=(faker.first_name_female(),faker.first_name_male()), length=1)[0],
        last_name=faker.last_name(),
        email=faker.ascii_free_email(),
        address=faker.address(),
        city=faker.city(),
        state=faker.state(),
        postal_code=faker.postcode(),
        country=faker.current_country(),
        phone=faker.msisdn(),
        created_at=datetime.now(),
    )

def create_product():
    return Products(
        name=faker.ecommerce_name(),
        price=faker.ecommerce_price(),
        description=faker.ecommerce_material() + ' ' + faker.ecommerce_category(),
        stock_quantity=faker.random_int(5, 999),
        weight=faker.numerify(text='%#.##'),
        created_at=datetime.now()
    )
def create_order(customer_id):
    return Orders(
        total_amount=faker.ecommerce_price(),
        shipping_address=faker.address(),
        city=faker.city(),
        state=faker.state(),
        postal_code=faker.postcode(),
        country=faker.current_country(),
        customer_id=customer_id,
        order_date=datetime.now(),
        status=faker.random_choices(elements=('pending', 'order created', 'order sent', 'shipped', 'delivered'), length=1)[0],
    )

def create_order_item(order_id, product_id, product_price):
    # generate random list
    return OrderItems(
        quantity=faker.random_int(1, 3),
        price=product_price,
        order_id=order_id,
        product_id=product_id
    )


def create_shipment(order_id, order_date):
    return Shipments(
        tracking_number=faker.bothify(text='????-########'),
        carrier=faker.random_choices(elements=('Sedan','Motorcycle','Van'), length=1)[0],
        order_id=order_id,
        shipment_date=order_date + timedelta(days=2),
        estimated_delivery_date=order_date + timedelta(days=5),
        status=faker.random_choices(elements=('in transit','at sorting hub','at delivery hub', 'delivered'), length=1)[0],
    )

def create_tracking_event(shipment_id):
    return TrackingEvents(
        location=faker.latlng(),
        event_description=faker.random_choices(elements=('package on route','package at sorting hub','package at delivery hub'), length=1)[0],
        shipment_id=shipment_id,
        event_date=faker.date(),
    )

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle_sigterm)
    Base.metadata.create_all(engine)

    faker = Factory.create()
    faker.add_provider(faker_commerce.Provider)

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        while True:
            customer = create_customer()
            session.add(customer)
            session.flush()
            product_no = faker.random_int(1, 3)
            product_list = [create_product() for _ in range(product_no)]
            session.add_all(product_list)
            session.flush()
            order = create_order(customer.customer_id)
            session.add(order)
            session.flush()
            order_item_list = [create_order_item(order.order_id, product.product_id, product.price) for product in product_list]
            session.add_all(order_item_list)
            session.flush()
            shipment = create_shipment(order.order_id, order.order_date)
            session.add(shipment)
            session.flush()
            tracking_event = create_tracking_event(shipment.shipment_id)
            session.add(tracking_event)
            session.flush()
            session.commit()
    except KeyboardInterrupt:
        session.close()
        logging.info('Exiting application..')
        

    

