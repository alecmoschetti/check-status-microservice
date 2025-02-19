from flask import Flask, request
import requests
import json

app = Flask(__name__)


@app.post("/check-status")
def check_url_status():
    url_payload = request.get_json()
    url_to_check = url_payload.get("url")
    error = None
    payload = dict()

    if url_to_check:
        try:
            res = requests.get(url_to_check)
            payload["status"] = res.status_code
            payload["is_up"] = res.status_code == requests.codes.ok
        except requests.RequestException as err:
            # base exception that should catch all specific requests errors
            # For more specific error codes: https://requests.readthedocs.io/en/latest/api/#exceptions
            error = str(err)  # str() is necessary to encode properly with json
    else:
        error = "Missing the url parameter in the original POST request."

    payload["error"] = error
    return json.dumps(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
