"""API calls from com.masterlock.api.client.AccountClient"""
from master_lock_api import BASE_URL, call_api


# @POST("/v4/account/authenticate")
# public abstract Observable<AuthResponse> \
#     authenticateCredentials(@Query("apikey") String paramString,
#                             @Body AuthRequest paramAuthRequest);
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
