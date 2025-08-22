import requests
from requests.auth import HTTPBasicAuth

def clear_rabbitmq_http():
    host = '192.168.1.206'
    port = 15671
    auth = HTTPBasicAuth('guest', 'guest')
    
    # Удалить все очереди
    queues = requests.get(f'http://{host}:{port}/api/queues', auth=auth).json()
    for queue in queues:
        requests.delete(f'http://{host}:{port}/api/queues/%2F/{queue["name"]}', auth=auth)
    
    # Удалить все exchanges (кроме системных)
    exchanges = requests.get(f'http://{host}:{port}/api/exchanges', auth=auth).json()
    for exchange in exchanges:
        if not exchange['name'].startswith('amq.') and exchange['vhost'] == '/':
            requests.delete(f'http://{host}:{port}/api/exchanges/%2F/{exchange["name"]}', auth=auth)

clear_rabbitmq_http()