import requests

from settings import (
    SERVICES,
    DATA_LAYER
)


def get_service_adapter(service_name):
    for service_adapter in SERVICES:
        if service_adapter[0] == service_name:
            return service_adapter
    return None


def get_service_adapter_url(service_name):
    service_adapter = get_service_adapter(service_name)
    if service_adapter:
        return f"{service_adapter[1]}:{service_adapter[2]}"
    raise ValueError(f"Service adapter {service_name} not found.")


def is_service_reachable(service_name):
    try:
        response = requests.get({get_service_adapter_url(service_name)})
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Service {service_name} is not reachable.\nError: {e}")
    return True
