import requests

from settings import (
    SERVICE_ADAPTERS,
    DATA_LAYER
)


def get_service_adapter(service_name):
    for service_adapter in SERVICE_ADAPTERS:
        if service_adapter[0] == service_name:
            return service_adapter
    return None


def get_service_adapter_url(service_name):
    service_adapter = get_service_adapter(service_name)
    if service_adapter:
        return f"{service_adapter[1]}:{service_adapter[2]}"
    raise ValueError(f"Service adapter {service_name} not found.")


def get_data_layer():
    return DATA_LAYER


def get_data_layer_url():
    data_layer = get_data_layer()
    return f"{data_layer[1]}:{data_layer[2]}"


def is_service_reachable(service_name):
    try:
        response = requests.get(f"http://{get_service_adapter_url(service_name)}/")
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Service {service_name} is not reachable.\nError: {e}")
    return True
