from prometheus_client import Counter, Histogram, REGISTRY
import time

METRICS_ENABLED = True

request_count = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

def metrics_response():
    from prometheus_client import REGISTRY, generate_latest
    return generate_latest(REGISTRY)
