import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Get RabbitMQ connection details from environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')  # RabbitMQ Host
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')      # RabbitMQ Username
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')  # RabbitMQ Password
RABBITMQ_API_URL = f'http://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:15672/api/queues'  # RabbitMQ API URL

# Prometheus metrics to expose for each queue (host, vhost, queue name)
queue_messages = Gauge('rabbitmq_individual_queue_messages', 'Total count of messages in the queue', ['host', 'vhost', 'name'])
queue_messages_ready = Gauge('rabbitmq_individual_queue_messages_ready', 'Count of ready messages in the queue', ['host', 'vhost', 'name'])
queue_messages_unacknowledged = Gauge('rabbitmq_individual_queue_messages_unacknowledged', 'Count of unacknowledged messages in the queue', ['host', 'vhost', 'name'])

def fetch_queue_stats():
    """
    Fetch queue statistics from RabbitMQ HTTP API and update Prometheus metrics.
    """
    try:
        # Make a GET request to fetch the queue stats from RabbitMQ
        response = requests.get(RABBITMQ_API_URL)
        
        if response.status_code == 200:
            # Parse the JSON response
            queues = response.json()
            
            for queue in queues:
                # Extract the necessary queue details
                host = RABBITMQ_HOST
                vhost = queue['vhost']
                name = queue['name']
                messages = queue['messages']
                messages_ready = queue['messages_ready']
                messages_unacknowledged = queue['messages_unacknowledged']
                
                # Update Prometheus metrics with the fetched data
                queue_messages.labels(host=host, vhost=vhost, name=name).set(messages)
                queue_messages_ready.labels(host=host, vhost=vhost, name=name).set(messages_ready)
                queue_messages_unacknowledged.labels(host=host, vhost=vhost, name=name).set(messages_unacknowledged)
        else:
            print(f"Failed to fetch data: {response.status_code}")
    
    except Exception as e:
        print(f"Error fetching queue stats: {e}")

def main():
    """
    Start the Prometheus HTTP server and periodically fetch queue statistics.
    """
    # Start Prometheus server on port 8000 to expose the metrics
    start_http_server(8000)
    
    # Periodically fetch and update the queue stats every 60 seconds
    while True:
        fetch_queue_stats()
        time.sleep(60)  # Update every minute

if __name__ == '__main__':
    main()
