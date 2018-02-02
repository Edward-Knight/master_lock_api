"""Package to interact with the Master Lock API."""
import json
import logging

import requests


LOGGER = logging.getLogger("master_lock_api")
"""Logger that this module uses."""

BASE_URL = "https://api.masterlockvault.com/"
"""The base URL for the Master Lock REST API."""


class MasterLockError(Exception):
    """Base exception for this module."""


def call_api(method, url, parameters=None, body=None):
    """Wrapper to interact with the Master Lock API. Returns deserialised JSON.
    """
    if method == "GET":
        request_func = requests.get
    elif method == "POST":
        request_func = requests.post
    elif method == "PUT":
        request_func = requests.put
    else:
        raise MasterLockError("HTTP method '" + method + "' is not supported.")

    response = request_func(url, params=parameters, json=body)
    if response.status_code != 200:
        raise MasterLockError(method + " to '" + url + "' failed with error '"
                              + str(response.status_code) + "':\n"
                              + response.text)

    response_json = response.json()
    LOGGER.debug(method + " to '" + url + "' returned:\n"
                 + json.dumps(response_json, indent=4, sort_keys=True))
    return response_json
