HOST="localhost"
PORT="5003"


BASE_URL = "http://localhost"
SERVICE_ADAPTERS = [
    ("shortenrest", BASE_URL, "5006"),
    ("rebrandly", BASE_URL, "5004"),
    ("tinyurl", BASE_URL, "5002"),
]
DATA_LAYER = ("data_layer", BASE_URL, "5000")
