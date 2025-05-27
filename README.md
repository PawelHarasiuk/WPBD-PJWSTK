# WPBD

This project implements a data processing pipeline using Apache Kafka, Apache Spark, PostgreSQL, and MinIO. It includes a Debezium connector for CDC (Change Data Capture) and Kafka UI for monitoring.

---

## Prerequisites

- Docker
- Docker Compose
- Git

---

## Project Setup

### Clone the Repository

```bash
git clone git@github.com:PawelHarasiuk/WPBD-PJWSTK.git
cd WPBD-PJWSTK
```

###
### Running the Application

Start all services using Docker Compose:

```bash
docker compose up -d
```
This command will start the following services:

- Kafka Cluster (3 nodes)
- Kafka UI (available at http://localhost:8080)
- PostgreSQL
- Debezium Connect
- Spark Master and Worker
- MinIO (Object Storage)
- Python data initialization service
- Service Endpoints

### You can monitor the Kafka cluster and topics using the Kafka UI interface:
👉 http://localhost:8080
## You can see data in minIO
👉 http://localhost:9001

Stopping the Application

To stop all services:

```bash
docker compose down
```
To stop and remove all volumes (this will delete all data):
```bash
docker compose down -v
```
