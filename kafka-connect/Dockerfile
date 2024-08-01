FROM confluentinc/cp-kafka-connect:7.4.5
USER root
COPY ./scripts/build-connectors.sh /etc/kafka/scripts/build-connectors.sh
RUN chmod +x /etc/kafka/scripts/build-connectors.sh
ENTRYPOINT /etc/kafka/scripts/build-connectors.sh