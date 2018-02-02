"""API calls from com.masterlock.api.client.ProductClient"""
from master_lock_api import BASE_URL, call_api


# @GET("/v4/kmsdevice/{id}/getavailablefirmwareversions")
# public abstract FirmwareDevAllAvailableResponse \
#     getAllFirmwareUpdates(@QueryMap Map<String, String> paramMap,
#                           @Path("id") String paramString);
def get_available_firmware_versions(username, api_key, some_id):
    raise NotImplementedError
    # doesn't work

    method = "GET"
    url = BASE_URL + "v4/kmsdevice/" + some_id + "/getavailablefirmwareversions"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    return call_api(method, url, parameters)

# @GET("/v4/kmsdevice/{id}/firmwareupdate")
# public abstract FirmwareUpdateResponse \
#     getFirmwareUpdate(@QueryMap Map<String, String> paramMap1,
#                       @Path("id") String paramString,
#                       @QueryMap Map<String, String> paramMap2);
def get_firmware_update(username, api_key, kms_id):
    raise NotImplementedError
    # must be owner
    # works, but fails with error '400':
    # {"Message":"100.2::No firmware available"}

    method = "GET"
    url = BASE_URL + "v4/kmsdevice/" + kms_id + "/firmwareupdate"
    parameters = {
        "username": username,
        "apikey": api_key,
        "appBuildId": 1,
        "appName": "androidble"
    }
    return call_api(method, url, parameters)

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

# @GET("/v4/product/{id}")
# public abstract ProductResponse \
#     getProduct(@QueryMap Map<String, String> paramMap,
#     @Path("id") String paramString);
def get_product(username, api_key, product_id):
    """API call to get information about a single product registered with the
    account.
    """
    method = "GET"
    url = BASE_URL + "v4/product/" + product_id
    parameters = {
        "username": username,
        "apikey": api_key
    }
    return call_api(method, url, parameters)

# @GET("/v4/product?complex=false")
# public abstract List<ProductResponse> \
#     getProducts(@QueryMap Map<String, String> paramMap);
def get_products(username, api_key):
    """API call to get a list of products registered with the account."""
    method = "GET"
    url = BASE_URL + "v4/product?complex=true"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    response_json = call_api(method, url, parameters)

    products = []
    for product in response_json:
        products.append({
            "name": product["Name"],
            "product_id": product["Id"],
            "device_id": product["KMSDevice"]["DeviceId"],
            "KMS_id": product["KMSDevice"]["Id"],
            "latitude": product["KMSDevice"]["Location"]["Latitude"],
            "longitude": product["KMSDevice"]["Location"]["Longitude"],
            "primary_code": product["KMSDevice"]["PrimaryCode"],
            "model_id": product["Model"]["Id"],
            "model_name": product["Model"]["Name"],
            "model_number": product["Model"]["ModelNumber"],
            "model_SKU": product["Model"]["SKU"]
        })
    return products

# @GET("/v4/kmsdevice/{id}/getspecifiedfirmwareupgrade")
# public abstract FirmwareUpdateResponse getSpecifiedFirmwareUpdate(
#     @QueryMap Map<String, String> paramMap,
#     @Path("id") String paramString,
#     @Query("deviceFirmwareVersion") int paramInt1,
#     @Query("requestedFirmwareVersion") int paramInt2);
def get_specified_firmware_upgrade(username, api_key, kms_id,
                                   current_firmware_version: int,
                                   requested_firmware_version: int):
    raise NotImplementedError
    # can't get this working
    # current firmware version is 1445277336
    # that's a valid UNIX timestamp for 2015-10-19T17:55:36+00:00

    method = "GET"
    url = BASE_URL + "v4/kmsdevice/" + kms_id + "/getspecifiedfirmwareupgrade"
    parameters = {
        "username": username,
        "apikey": api_key,
        # paramLock.getFirmwareVersion()
        "deviceFirmwareVersion": current_firmware_version,
        "requestedFirmwareVersion": requested_firmware_version
    }
    return call_api(method, url, parameters)
