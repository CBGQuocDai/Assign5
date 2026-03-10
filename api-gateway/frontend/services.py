import requests
from django.conf import settings


def call_service(service_name, path, method='GET', data=None, params=None):
    """Single helper to proxy calls to micro-services."""
    base = settings.SERVICES.get(service_name, '')
    url = f"{base}{path}"
    try:
        if method == 'GET':
            resp = requests.get(url, params=params, timeout=5)
        elif method == 'POST':
            resp = requests.post(url, json=data, timeout=5)
        elif method == 'PUT':
            resp = requests.put(url, json=data, timeout=5)
        elif method == 'PATCH':
            resp = requests.patch(url, json=data, timeout=5)
        elif method == 'DELETE':
            resp = requests.delete(url, timeout=5)
            return None
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None
