from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
from flasgger import Swagger, swag_from

from settings import HOST, PORT
from utilities import get_service_adapter_url_list
from communications import (
    create_short_url,
    save_short_url,
    get_short_url,
    get_token_list,
    delete_short_url,
    delete_short_url_from_data_layer,
    get_short_url_list,
)

template = {
    "info":{
        "title": "URL Handler",
        "description": "URL handler for creating, deleting and listing URLs."
    }
}

app = Flask(__name__)
swagger = Swagger(app, template=template)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/create_short_url", methods=["POST"])
@swag_from("flasgger_docs/create_short_url_endpoint.yml")
def create_short_url_endpoint():
    url = request.json.get("url", "")
    alias = request.json.get("alias", "")
    user_id = request.json.get("user_id", "")
    note = request.json.get("note", "")
    preferred_service = request.json.get("preferred_service", "")
    
    try:
        service_url_list = get_service_adapter_url_list(preferred_service)
    except ValueError as e:
        return {"data": {}, "errors": [str(e)], "code": 422}, 422
    
    response, service_name = create_short_url(service_url_list, url, alias, user_id)
    
    if response.get("errors"):
        return response, response["code"]
    
    data_layer_response = save_short_url(url, response["data"]["short_url"], user_id, note, service_name)

    if data_layer_response.get("errors"):
        return data_layer_response, data_layer_response["code"]
    
    return {"data": data_layer_response["data"], "errors": [], "code": 200}, 200


@app.route("/get_short_url_list", methods=["GET"])
@swag_from("flasgger_docs/get_short_url_list_endpoint.yml")
def get_short_url_list_endpoint():
    user_id = request.args.get("user_id", "")
    response = get_short_url_list(user_id)
    if response.get("errors"):
        return response, response["code"]
    return {"data": response["data"], "errors": [], "code": 200}, 200


@app.route("/delete_short_url", methods=["DELETE"])
@swag_from("flasgger_docs/delete_short_url_endpoint.yml")
def delete_short_url_endpoint():
    short_url_id = request.args.get("short_url_id", "")
    user_id = request.args.get("user_id", "")
    
    short_url = get_short_url(short_url_id, user_id)

    if short_url.get("errors"):
        return short_url, short_url["code"]
    
    service_name = short_url["data"]["service"]

    token_list_obj = get_token_list(user_id)
    token_list = token_list_obj["data"]["token_list"]
    found_token = ""
    for token in token_list:
        if token["name"] == service_name:
            found_token = token["token"]
            break
    if not token:
        return {"data": {}, "errors": ["No token found for service"], "code": 422}, 422
    
    response = delete_short_url(short_url["data"]["short_url"], found_token, service_name)

    if response.get("errors"):
        return response, response["code"]
    
    data_layer_response = delete_short_url_from_data_layer(short_url_id, user_id)

    if data_layer_response.get("errors"):
        return data_layer_response, data_layer_response["code"]
    
    return {"data": {}, "errors": [], "code": 200}, 200


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
