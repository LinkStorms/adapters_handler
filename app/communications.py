import requests

from utilities import get_data_layer_url, get_service_adapter_url_by_name


def create_short_url(service_url_list, url, alias, user_id):
    token_list_obj = get_token_list(user_id)
    if token_list_obj.get("errors"):
        return token_list_obj, None
    token_list = token_list_obj["data"]["token_list"]
    available_service_name_list = [token["name"] for token in token_list]
    available_service_list = list(filter(lambda x: x[0] in available_service_name_list, service_url_list))
    if not available_service_list:
        return {"data": {}, "errors": ["No service available"], "code": 422}, None
                
    body = {
        "url": url,
        "alias": alias
    }
    for service_name, service_url in available_service_list:
        for token in token_list:
            if token["name"] == service_name:
                body["token"] = token["token"]
                break
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


def get_short_url(short_url_id, user_id, data_layer_url=get_data_layer_url()):
    response = requests.get(data_layer_url + "/get_short_url", params={"short_url_id": short_url_id, "user_id": user_id})
    return response.json()


def get_token_list(user_id, data_layer_url=get_data_layer_url()):
    response = requests.get(data_layer_url + "/token_list", params={"user_id": user_id})
    return response.json()


def delete_short_url(alias, token, service_name, data_layer_url=get_data_layer_url()):
    body = {
        "alias": alias,
        "token": token
    }
    service_url = get_service_adapter_url_by_name(service_name)
    response = requests.delete(service_url + "/delete", json=body)
    return response.json()


def delete_short_url_from_data_layer(short_url_id, user_id, data_layer_url=get_data_layer_url()):
    response = requests.get(data_layer_url + "/delete_short_url", params={"short_url_id": short_url_id, "user_id": user_id})
    return response.json()


def get_short_url_list(user_id, data_layer_url=get_data_layer_url()):
    response = requests.get(data_layer_url + "/short_url_list", params={"user_id": user_id})
    return response.json()
