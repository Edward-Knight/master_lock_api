"""API calls from com.masterlock.api.client.ProductInvitationClient"""
from master_lock_api import BASE_URL, call_api


# @GET("/v4/kmsdevice/{id}/servicecode")
# public abstract TempCodeResponse \
#     getTempCode(@QueryMap Map<String, String> paramMap,
#                 @EncodedQuery("accessTime") String paramString1,
#                 @Path("id") String paramString2);
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
