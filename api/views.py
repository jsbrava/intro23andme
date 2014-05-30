from django.http import HttpResponse
from django.shortcuts import redirect

import json
import logging
log = logging.getLogger("api")

# import our OAuth client
import client


def profiles(request):
    c = client.OAuthClient(request.session[client.OAUTH_KEY])
    data = c.get_profiles()
    return HttpResponse(data, mimetype="application/json")

def user(request):
    c = client.OAuthClient(request.session[client.OAUTH_KEY])
    data = c.get_user()
    return HttpResponse(data, mimetype="application/json")

def login(request):
    return redirect(client.LOGIN_URL)
    
"""
The 23andMe api calls this view with a ?code=xxxxxx paramter.  This parameter is a short lived authorization code that you must use to get a an OAuth authorization token which you can use to retrieve user data.  This view users database backed session to store the auth token instead of cookies in order to protect the token from leaving the server as it allows access to significant sensitive user information.
"""
def callback(request):
    c = client.OAuthClient()
    code = request.GET["code"]
    log.debug("code: %s" % code)

    log.debug("fetching token...")

    (access_token, refresh_token) = c.get_token(code)
    log.debug("access_token: %s refresh_token: %s" % (access_token, refresh_token))

    log.debug("refreshing token...")

    (access_token, refresh_token) = c.refresh_token(refresh_token)
    log.debug("access_token: %s refresh_token: %s" % (access_token, refresh_token))

    request.session[client.OAUTH_KEY] = access_token

    c = client.OAuthClient(request.session[client.OAUTH_KEY])
    names_json = c.get_name_profile()
    names = json.loads(names_json)
    print "callback names: ", names
    request.session["account_id"] = names['id']
    request.session["name"] = "%s %s" % (names['first_name'], names['last_name'])
    log.debug("account_id: %s name: %s" % (request.session["account_id"], request.session["name"]))
    return redirect("/results")

def logout(request):
    log.debug("logging out...")
    request.session.clear()
    return redirect("/")
