#!/usr/bin/env python3
"""Module for interacting with the Master Lock API."""
import argparse
import datetime
from datetime import datetime as dt
import logging
import json
import pprint
import signal
import sys

import requests

LOGGER = logging.getLogger("master_lock_api")
"""Logger that this module uses."""

BASE_URL = "https://api.masterlockvault.com/"
"""The base URL for the Master Lock REST API."""


class MasterLockError(Exception):
    """Base exception for this module."""


def load_config(config_file):
    """Parse the config file as JSON."""
    try:
        with open(config_file) as f:
            new_config = json.load(f)
        LOGGER.info("Loaded config '" + config_file + "'")
        return new_config
    except FileNotFoundError:
        LOGGER.info("Config file '" + config_file + "' not found")
        return {}


def save_config(config, config_file):
    """Serialise the config to file in a pretty JSON format."""
    with open(config_file, "w") as f:
        json.dump(config, f, sort_keys=True, indent=2)
    LOGGER.info("Saved config '" + config_file + "'")


def call_api(method, url, parameters=None, body=None):
    """Wrapper to interact with the Master Lock API. Returns deserialised JSON.
    """
    if method == "GET":
        request_func = requests.get
    elif method == "POST":
        request_func = requests.post
    else:
        raise MasterLockError("HTTP method '" + method + "' is not supported.")

    response = request_func(url, params=parameters, json=body)
    if response.status_code != 200:
        raise MasterLockError(method + " to '" + url + "' failed with error '"
                              + str(response.status_code) + "':\n"
                              + response.text)

    response_json = response.json()
    LOGGER.debug(method + " to '" + url + "' returned:\n"
                 + pprint.pformat(response_json))
    return response_json


def get_api_key(username, password):
    """API call to get an API key to use in future requests."""
    method = "POST"
    url = BASE_URL + "v4/account/authenticate/"
    parameters = {"apikey": "androidble"}
    body = {
        "username": username,
        "password": password
    }
    response_json = call_api(method, url, parameters, body)
    return response_json["Token"]


def get_kms_ids(username, api_key):
    """API call to get lock KMS id's associated with the account."""
    method = "GET"
    url = BASE_URL + "v4/kmsdevicekey/"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    response_json = call_api(method, url, parameters)

    locks = []
    for lock in response_json:
        locks.append({
            "device_id": lock["DeviceId"],
            "KMS_id": lock["KMSDeviceId"]
        })
    return locks


def generate_temporary_code(username, api_key, kms_id, access_time=None):
    """API call to generate a temporary code. If access_time is None, gets a
    currently active code.
    """
    method = "GET"
    url = BASE_URL + "v4/kmsdevice/" + kms_id + "/servicecode/"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    if access_time is not None:
        parameters["accessTime"] = access_time
    response_json = call_api(method, url, parameters)
    return response_json["ServiceCode"]


def load_and_check_config(config_file):
    """Loads a JSON config file, checks all the required values have been
    provided, fetches any missing data using the Master Lock API and saves the
    config back to file before returning it.
    """
    # set up default config skeleton to avoid key errors
    config = {
        "API_key": "",
        "locks": [],
        "username": "",
        "password": ""
    }
    config.update(load_config(config_file))
    # fill out config file information where missing, or error
    try:
        if config["username"] == "":
            raise MasterLockError("No 'username' supplied in config file.")
        if config["API_key"] == "":
            if config["password"] == "":
                raise MasterLockError("No 'password' or 'API_key' supplied in "
                                      "config file.")
            LOGGER.info("No API key, getting from Master Lock API...")
            config["API_key"] = get_api_key(config["username"],
                                            config["password"])
        if config["locks"] == []:
            LOGGER.info("No known locks, getting from Master Lock API...")
            config["locks"] = get_kms_ids(config["username"], config["API_key"])
    finally:
        save_config(config, config_file)
    return config


def main():
    """Command-line entry point."""
    # quit without raising a KeyboardInterrupt exception
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # parse command-line arguments
    parser = argparse.ArgumentParser(description="Generates temporary codes "
                                                 "using the Master Lock API.")
    # todo: add argument to specify number of codes or specific access_time
    parser.add_argument("--config", default="config.json",
                        help="JSON config file (defaults to %(default)s). "
                             "Will be created if missing.")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="show debugging logs")
    args = parser.parse_args()

    # set up LOGGER
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    LOGGER.addHandler(handler)
    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    # load config
    try:
        config = load_and_check_config(args.config)
    except Exception as e:
        LOGGER.exception("Error whilst loading config: " + str(e),
                         exc_info=not isinstance(e, MasterLockError))
        sys.exit(-1)

    # select lock
    prompt = "Please select lock to generate codes for:\n"
    kms_ids = {}
    for i, lock in enumerate(config["locks"]):
        number = str(i + 1)
        prompt += number + ")\t" + lock["device_id"] + "\n"
        kms_ids[number] = lock["KMS_id"]
    prompt += "> "
    while True:
        answer = input(prompt)
        if answer in kms_ids:
            kms_id = kms_ids[answer]
            break

    # generate 10 years of codes starting from tomorrow
    access_time = dt.now().replace(hour=0, minute=0, second=0, microsecond=0) \
                  + datetime.timedelta(days=1)
    for i in range(21900):
        try:
            code = generate_temporary_code(
                config["username"], config["API_key"], kms_id, access_time)
            timestamp = access_time.strftime("%Y-%m-%d_%H")
            print(code, timestamp)
        except Exception as e:
            LOGGER.exception("Error whilst generating temporary code "
                             + str(i) + ": " + str(e),
                             exc_info=not isinstance(e, MasterLockError))
        access_time += datetime.timedelta(hours=4)  # new code available


if __name__ == "__main__":
    main()
