from flask import Flask, json, request
from werkzeug.exceptions import HTTPException

from settings import HOST, PORT
from utilities import get_service_adapter_url_list
from communications import (
    create_short_url,
    save_short_url
)


app = Flask(__name__)


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
def create_short_url_endpoint():
    url = request.json.get("url", "")
    alias = request.json.get("alias", "")
    token = request.json.get("token", "")
    user_id = request.json.get("user_id", "")
    note = request.json.get("note", "")
    preferred_service = request.json.get("preferred_service", "")
    
    try:
        service_url_list = get_service_adapter_url_list(preferred_service)
    except ValueError as e:
        return {"data": {}, "errors": [str(e)], "code": 422}, 422
    
    response, service_name = create_short_url(service_url_list, url, alias, token)
    
    if response.get("errors"):
        return response, response["code"]
    
    data_layer_response = save_short_url(url, response["data"]["short_url"], user_id, note, service_name)

    if data_layer_response.get("errors"):
        return data_layer_response, data_layer_response["code"]
    
    return {"data": response["data"], "errors": [], "code": 200}, 200



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
