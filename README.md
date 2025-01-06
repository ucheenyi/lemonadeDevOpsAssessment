# lemonadeDevOpsAssessment
Lemonade DevOps Assessment Scripts

##Rabbit MQ Exporter

Running the Exporter:
Set the required environment variables for RabbitMQ connection:

export RABBITMQ_HOST=your_rabbitmq_host
export RABBITMQ_USER=your_rabbitmq_user
export RABBITMQ_PASSWORD=your_rabbitmq_password

Run the Python script:

python rabbitmq_exporter.py

Make sure no other service is rumnning on Port 8000
This script will start a Prometheus-compatible metrics server on http://localhost:8000/metrics, and the RabbitMQ metrics will be updated every minute.
