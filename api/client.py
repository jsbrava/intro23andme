import requests   # pip install requests to get it
import urllib 
import json
from django.http import HttpResponse
#from members.models import User
import logging
log = logging.getLogger("api_client")
# Get the token using a POST request and a code
 
from django.conf import settings

SCOPE = "names relatives introduction:write introduction:read"

# leave these alone
#BASE_URL = "https://api.23andme.com/1/demo/"
BASE_URL = "https://api.23andme.com/1/"
LOGIN_URL = "https://api.23andme.com/authorize/?redirect_uri=%s&response_type=code&client_id=%s&scope=%s" % (settings.CALLBACK_URL, settings.CLIENT_ID, SCOPE)
OAUTH_KEY = "access_token"

class OAuthClient(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_token(self, authorization_code):
        parameters = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': authorization_code, # the authorization code obtained above
            'redirect_uri': settings.CALLBACK_URL,
            'scope': SCOPE,
        }
        response = requests.post(
            "https://api.23andme.com/token/",
            data = parameters
        )

        print "get_token_response.json: %s" % response.json()
        if response.status_code == 200:
            return (response.json()['access_token'], response.json()['refresh_token'])
        else:
            response.raise_for_status()

    def refresh_token(self, refresh_token):
        parameters = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'redirect_uri': settings.CALLBACK_URL,
            'scope': SCOPE,
        }
        response = requests.post(
            "https://api.23andme.com/token/",
            data = parameters
        )

        #print "response.json: %s" % response.json()
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return (response.json()['access_token'], response.json()['refresh_token'])
        else:
            response.raise_for_status()

    def _get_resource(self, resource):
        if self.access_token is None:
            raise Exception("access_token cannot be None")

        headers = {'Authorization': 'Bearer %s' % self.access_token}
        url = "%s%s" % (BASE_URL, resource)
        
        response = requests.get(
            url,
            headers=headers,
            verify=False,
        )
        #print "_get_resource url: %s" % url
        #print "response get response: %s" % response
        #print "response get text: %s" % response.text
        #print "response get status_code: %s" % response.status_code
        #print "response: %s" % response
        #print "response.json: %s" % response.json()
        #print "response.text: %s" % response.text
        if response.status_code == 200:
            log.debug('_get_resource url: %s response: %s', url, response)
            return response.text
        else:
            log.debug('_get_resource error url: %s response: %s', url, response)
            response.raise_for_status()
            return response.text
            
    def _post_resource(self, resource, body):
        if self.access_token is None:
            raise Exception("access_token cannot be None")

        headers = {'Authorization': 'Bearer %s' % self.access_token,
                   #'Content-Type' : 'application/octet-stream'}
                   'Content-Type' : 'text/plain'}
        url = "%s%s" % (BASE_URL, resource)
        response = requests.post(
            url,
            headers=headers,
            verify=False,
            data=body,
        )
        #log.debug("response.status_code: %s" % response.status_code)
        #log.debug('response.text: %s' % response.text)
        #log.debug('response.raw: %s' % response.raw)
        #log.debug('response headers: %s' % headers)
        if response.status_code == 200 and response.text != '500 error':
            log.debug('_post_resource url: %s response: %s .text: %s' ,url, response, response.text)
            return response.text
        else:
            #response.raise_for_status()
            log.debug('_post_resource error url: %s response: %s .text: %s' ,url, response, response.text)
            return response.text
            
    def get_user(self): 
        return self._get_resource("user/")

    def get_name_profile(self):
        return self._get_resource("names/")
    
    def get_relatives(self, profile_id):
        relatives = 'relatives/' + str(profile_id) + '/?limit=00'
        return self._get_resource(relatives)
    
    def post_intro(self, profile_id, match_id, intro_text):
        if match_id == None:   # this happens if you try to send to yourself
            return False
        #u = User()     # I'm not sure my resend function was a good idea
        #if u.too_soon(match_id) == True:
        #    return False
        intro = 'introduction/' + str(profile_id) + '/' + str(match_id) + '/'
        body = 'visibility=genome' + '&message_text=' + intro_text
        response = self.get_send_status(profile_id, match_id)
        
        if response["introduction"]["status"] == "rejected" or response["introduction"]["visibility"] == "genome":
            log.debug('post_intro rejected response: %s match_id: %s', response, match_id)
            return False 
        
        if response["can_send"] == True:
            #log.debug('post_intro can send response: %s match_id: %s', response, match_id)
            #return True    #for testing
            response = json.loads(self._post_resource(intro, body))
            if response["introduction"]["status"] == "sent":
                log.debug('post_intro post sent response: %s match_id: %s', response, match_id)
                response = self.get_send_status(profile_id, match_id)
                return True
            else:
                log.debug('post_intro post not sent response: %s match_id: %s', response, match_id)
                return False
        else:  #let's see if we can cancel and resend an introduction

            if response["introduction"]["status"] != "cancelled" and response["introduction"]["status"] != "accepted": 
                self.send_cancel(profile_id, match_id)      #cancel then resend the introduction
                if self.get_send_status(profile_id, match_id)["can_send"] == True:
                    response = json.loads(self._post_resource(intro, body))
                    if response["introduction"]["status"] == "sent":
                        log.debug('post_intro2 post sent response: %s match_id: %s', response, match_id)
                        return True
                    else:
                        log.debug('post_intro2 post not sent response: %s match_id: %s', response, match_id)
                        return False
                return False
            else:
                return False
        
    def get_send_status(self, profile_id, match_id):
        intro = 'introduction/' + str(profile_id) + '/' + str(match_id)
        response = json.loads(self._get_resource(intro))
        if response["introduction"] == {}:
            response["introduction"]["status"] = 'none'
            response["introduction"]["visibility"] = 'none'
        log.debug('get_send_status intro: %s response: %s' ,intro, response)
        return response  #returns json
    
    def send_cancel(self, profile_id, match_id):
        if self.access_token is None:
            raise Exception("access_token cannot be None")
        
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        #url = "%s%s" % (BASE_URL, resource)
        url = BASE_URL + 'introduction/' + profile_id + '/' + match_id + '/?status=cancelled'
        #print "url", url
        #return True
        response = requests.patch(
            url,
            headers=headers,
            verify=False,
        )
        if response.status_code == 200 and response.text != '500 error':
            log.debug('send_cancel url: %s response: %s .text: %s' ,url, response, response.text)
            return True
        else:
            #response.raise_for_status("send cancel")
            log.debug('send_cancel error url: %s response: %s .text: %s' ,url, response, response.text)
            return False
    

