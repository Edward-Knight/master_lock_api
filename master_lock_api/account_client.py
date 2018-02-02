"""API calls from com.masterlock.api.client.AccountClient"""
from master_lock_api import BASE_URL, MasterLockError, call_api


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

# @POST("/v4/account/resetpassword")
# public abstract Response \
#     forgotPasscode(@Query("apikey") String paramString,
#                    @Body ForgotRequest paramForgotRequest);
def forgot_password(email):
    """API call that sends a password reset email to the specified address.
    Returns True if successful and False otherwise.

    Call this in a loop for fun!
    """
    method = "POST"
    url = BASE_URL + "v4/account/resetpassword"
    parameters = {
        "apikey": "androidble"
    }
    body = {"email": email}
    try:
        response_json = call_api(method, url, parameters, body)
        return isinstance(response_json, dict) \
               and "ServiceResult" in response_json \
               and response_json["ServiceResult"] == 1
    except MasterLockError:
        return False

# @POST("/v4/account/retrieveusername")
# public abstract Response \
#     forgotUsername(@Query("apikey") String paramString,
#                    @Body ForgotRequest paramForgotRequest);
def forgot_username(email):
    """API call that sends a username reminder email to the specified address.
    Returns True if successful and False otherwise.

    Call this in a loop for fun!
    """
    method = "POST"
    url = BASE_URL + "v4/account/retrieveusername"
    parameters = {
        "apikey": "androidble"
    }
    body = {"email": email}
    try:
        response_json = call_api(method, url, parameters, body)
        return isinstance(response_json, dict) \
               and "ServiceResult" in response_json \
               and response_json["ServiceResult"] == 1
    except MasterLockError:
        return False

# @GET("/v4/account/emailverification/{id}")
# public abstract Object \
#     getEmailVerificationDetails(@Query("apikey") String paramString1,
#                                 @Path("id") String paramString2);
def get_email_verification_details(id_):
    raise NotImplementedError
    # not working (maybe use the /v5/ version ?)
    # tried with all ids and only got {"Message":"100.6::Invalid ID."} and 404s

    method = "GET"
    url = BASE_URL + "v4/account/emailverification/" + id_
    parameters = {"apikey": "androidble"}
    return call_api(method, url, parameters)
