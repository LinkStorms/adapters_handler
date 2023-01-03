import copy

import requests

from settings import (
    SERVICE_ADAPTERS,
    DATA_LAYER
)


def get_service_adapter(service_name):
    for service_adapter in SERVICE_ADAPTERS:
        if service_adapter[0] == service_name:
            return service_adapter
    raise ValueError(f"Service adapter {service_name} not found.")


def get_service_adapter_url(service_adapter):
    if service_adapter:
        return f"{service_adapter[1]}:{service_adapter[2]}"
    raise ValueError(f"Service adapter {service_adapter[0]} not found.")


def get_data_layer_url():
    return f"{DATA_LAYER[1]}:{DATA_LAYER[2]}"


def get_service_adapter_url_list(preferred_service_name=None):
    if not preferred_service_name:
        return [get_service_adapter_url(service_adapter) for service_adapter in SERVICE_ADAPTERS]
    preferred_service = get_service_adapter(preferred_service_name)
    service_adapters = copy.deepcopy(SERVICE_ADAPTERS)
    try:
        service_adapters.remove(preferred_service)
        service_adapters.insert(0, preferred_service)
    except ValueError:
        pass
    return [get_service_adapter_url(service_adapter) for service_adapter in service_adapters]
        


def check_reachability(service_name, service_url):
    try:
        response = requests.get(service_url)
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Service {service_name} is not reachable.\nError: {e}")
    return True


def is_service_reachable(service_name):
    service_adapter = get_service_adapter(service_name)
    if service_adapter:
        service_url = get_service_adapter_url(service_name)
        return check_reachability(service_name, service_url)
    raise ValueError(f"Service adapter {service_name} not found.")


def is_data_layer_reachable():
    data_layer_url = get_data_layer_url()
    return check_reachability("data_layer", data_layer_url)
