#!/bin/bash

#
#apt-get update
#apt-get install -y \
#      curl \
#      dos2unix \
#      openjdk-17-jdk-headless \
#      procps \
#      gcc \
#      python3-dev \
#      libpq-dev \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*
#
echo "Waiting for services to be ready..."
echo "======"
echo | pwd
echo | ls
echo "Sending query to debizum"

until curl -s debezium:8083/connectors; do
  echo "Waiting for Debezium…"
  sleep 10
done

curl -X POST http://debezium:8083/connectors -H "Content-Type: application/json" --data @connector.json                                                                                           ─╯
sleep 30
echo "Finished setup"