"""API calls from com.masterlock.api.client.ProductClient"""
from master_lock_api import BASE_URL, call_api


# @GET("/v4/kmsdevicekey")
# public abstract List<KmsDeviceKeyResponse> \
#     getKmsDeviceKeys(@QueryMap Map<String, String> paramMap);
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
