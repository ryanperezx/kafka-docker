#!/bin/bash

echo "Launching Kafka Connect worker" 
/etc/confluent/docker/run & 
# Wait for Kafka Connect to finish building
echo "Waiting for Kafka Connect to start listening on localhost ⏳"
while : ; do
    curl_status="$(curl -s -o /dev/null -w %{http_code} http://localhost:8093/connectors)"
    echo -e $'(date)' " Kafka Connect listener HTTP state: " $curl_status " (waiting for 200)"
    if [[ "$curl_status" -eq 200 ]] ; then
    break
    fi
    sleep 5 
done
# Add connectors below here
curl -X POST -H "Content-type: application/json" -d @/etc/kafka/connect/plugins/sample-pg-connector.json "http://kafka-connect:8093/connectors"
sleep infinity