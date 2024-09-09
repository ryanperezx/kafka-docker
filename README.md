# Kafka-docker
This project focuses on setting up and learning three essential technologies for data streaming and monitoring, all integrated using Docker. This setups a postgres instance with some sample schemas, and a kafka connector.

* Kafka with KRaft Protocol: A lightweight, broker-only deployment of Apache Kafka that eliminates the need for Zookeeper, simplifying cluster management.

* [PostgreSQL with Debezium](https://debezium.io/documentation/reference/stable/connectors/postgresql.html): A Change Data Capture (CDC) solution using Debezium to stream real-time database changes from PostgreSQL into Kafka topics.

* [Kafka UI](https://github.com/provectus/kafka-ui): A web-based tool to monitor and manage Kafka brokers, topics, and consumer groups. 