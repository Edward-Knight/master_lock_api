"""API calls from com.masterlock.api.client.KMSDeviceClient"""
from master_lock_api import BASE_URL, call_api


# @GET("/v4/kmsdevice/{id}/mastercode")
# public abstract MasterBackupResponse \
#     getMasterBackupCode(@QueryMap Map<String, String> paramMap,
#                         @Path("id") String paramString);
def get_master_backup_code(username, api_key, kms_id):
    """API call that get the "master" or "backup" code.

    Must be the owner.
    Code will always start with "U" and be of length 11.
    """
    method = "GET"
    url = BASE_URL + "/v4/kmsdevice/" + kms_id + "/mastercode"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    return call_api(method, url, parameters)["MasterCode"]

# @PUT("/v4/kmsdevice/{id}")
# public abstract Response \
#     updateDeviceTraits(@QueryMap Map<String, String> paramMap,
#                        @Path("id") String paramString,
#                        @Body KmsUpdateTraitsRequest \
#                            paramKmsUpdateTraitsRequest);
def update_traits(username, api_key, kms_id):
    raise NotImplementedError
    # todo: work out traits
    # this currently works for changing the primary key server side

    method = "PUT"
    url = BASE_URL + "/v4/kmsdevice/" + kms_id
    parameters = {
        "username": username,
        "apikey": api_key
    }
    body = {
        "Id": kms_id,
        "Traits": [{
            "Name": "PRIMARYCODE",
            "Value": "URURURU",
                     "ULURURU"
# paramLock.getFirmwareCounter() <<32 | paramLock.getPrimaryCodeCounter()
            "Counter": 0
        }]
    }
    response_json = call_api(method, url, parameters, body)
    return isinstance(response_json, dict) \
           and "ServiceResult" in response_json \
           and response_json["ServiceResult"] == 1
