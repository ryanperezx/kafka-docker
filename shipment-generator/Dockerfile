FROM python:3.10.15-bookworm

WORKDIR shipment-generator
COPY . /shipment-generator
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "shipment-data-simulator.py"] 