import requests

from utilities import get_data_layer_url, get_service_adapter_url_by_name


def create_short_url(service_url_list, url, alias, token):
    body = {
        "url": url,
        "alias": alias,
        "token": token
    }
    for service_name, service_url in service_url_list:
        response = requests.post(service_url + "/create", json=body)
        if response.status_code == 200:
            return response.json(), service_name
    return response.json(), None


def save_short_url(url, alias, user_id, note, service_name, data_layer_url=get_data_layer_url()):
    body = {
        "long_url": url,
        "short_url": alias,
        "user_id": user_id,
        "note": note,
        "service": service_name
    }
    response = requests.post(data_layer_url + "/create_short_url", json=body)
    return response.json()
