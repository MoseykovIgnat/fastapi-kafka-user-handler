#!/bin/sh

echo "Wait for kafka started"

while ! kafkacat -b $KAFKA_HOST:$KAFKA_PORT -L; do
    sleep 0.1
done

echo "Kafka was successfully started"

exec "$@"