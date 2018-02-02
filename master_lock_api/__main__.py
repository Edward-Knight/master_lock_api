"""CLI script to interact with the Master Lock API."""
import argparse
import datetime
from datetime import datetime as dt
import json
import logging
import signal
import sys

from master_lock_api import LOGGER, MasterLockError
from master_lock_api.account_client import get_api_key
from master_lock_api.product_client import get_kms_ids
from master_lock_api.product_invitation_client import generate_temporary_code


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
