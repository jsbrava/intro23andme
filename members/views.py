from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
from django.template import RequestContext
#from members.models import User
from time import time  
import api.client
import forms
import json
import logging
log = logging.getLogger("members_views") 

@xframe_options_exempt
def get_started(request):
    myDict = {'client_id': settings.CLIENT_ID}
    return render_to_response("members/get_started.html", myDict)
    
def results(request):
    choices = {}
    choices['profiles'] = dict(_get_profile_choices(request))
    choices['BASE_URL'] = settings.BASE_URL
    print choices
    return render_to_response('members/profile.html', {'choices':choices},
                   context_instance=RequestContext(request))
    #return HttpResponse(choices, mimetype="application/json") 

def relatives(request):
    #GET relatives will get the profile_id then return all of the relative matches for that profile_id
    profile_id = request.POST.get("profile_id", "")
    #send = request.POST.get("send", "")  #send can either be 'new' or 'resend'
    #save the text so that we only have to get it one time
    request.session["intro_text"] = request.POST.get("introductionText", "")
    #print 'profile_id: ', profile_id,  intro_text
    print 'profile_id:', profile_id    ## ** should check. If profile_name is empty, nothing was clicked
    if profile_id == '':
        print 'nothing was clicked'
        #print request
        return HttpResponse("gotta pick a name")
    
    c = api.client.OAuthClient(request.session[api.client.OAUTH_KEY])
    if settings.DEBUG == True:
        f = open('23andMeRelativesJSON', 'w')
        f.write(c.get_relatives(profile_id))
        f.close
    result = c.get_relatives(profile_id)    
    log.debug('relatives: %s ' % result) 
    return HttpResponse(result, content_type="application/json")

def send_intro(request):
    profile_id = request.POST.get("profile_id", "")
    match_id = request.POST.get("match_id", "")
    #I don't think a send selector is needed
    #send = request.POST.get("send", "")
    c = api.client.OAuthClient(request.session[api.client.OAUTH_KEY])
    #if send == 'resend':
    #    status = c.send_cancel(profile_id, match_id)
    #status = c.send_cancel(profile_id, match_id)
        #do a patch to cancel the old introduction so that we can send again
    status = c.post_intro(profile_id, match_id, request.session["intro_text"])
    log.debug('send_intro status %s ' % status)
    return HttpResponse(json.dumps({'send':status}), content_type="application/json")
  
def get_relatives(request):
    t = time()    #get the current time to see how long this takes
    profile_name = request.POST.get("profile_name", "")
    ## ** should check. If profile_name is empty, nothing was clicked
    if profile_name == '':
        print 'nothing was clicked'
        temp = ' | '.split('|')   #ends up with nothing selected but shouldn't die
    else:
        temp = profile_name.split('|')   #split into profile_id and name
    intro_text = request.POST.get("introductionText", "")
    
    profile_id = temp[0]
    sender_name = temp[1]   #not using but could use it to sign the text
    #print 'profile_id: ', profile_id, sender_name, intro_text
    #print 'name: ', name, 'intro_text', intro_text
    send = request.POST.get("send", "")
    c = api.client.OAuthClient(request.session[api.client.OAUTH_KEY])
    relatives_json = c.get_relatives(profile_id)
    relatives = json.loads(relatives_json)
    counter = 0
    not_counter = 0
    total_count = relatives['count']
    
    for relative in relatives['relatives']:
        if counter >= settings.INTRO_NUM:
            break
        
        if send == 'new':
            #if relative['intro_status'] == None and relative['share_status'] != 'Sharing Genomes' and relative['share_status'] != 'Owned Profile':
            #if relative['share_status'] == 'Owned Profile':
            if relative['last_name'] == 'Delane' and relative['first_name'] == 'June':  
                status = c.post_intro(profile_id, relative['match_id'], _update_text(intro_text, relative['first_name']))
                if  status == 'sent':
                    counter += 1
                else:
                    not_counter += 1
                print 'get_relatives1: ', status, relative['intro_status'], relative['share_status'], relative['first_name'], relative['last_name'], profile_id, relative['match_id'] 
                #_test_intro_relatives(request, profile_id, relative['match_id'])
        elif send == 'resend':
            if relative['share_status'] != 'Sharing Genomes' and relative['share_status'] != 'Owned Profile':  
                status = c.post_intro(profile_id, relative['match_id'], _update_text(intro_text, relative['first_name']))
                if  status == 'sent':
                    counter += 1
                else:
                    not_counter += 1
                print 'get_relatives2: ', status, relative['intro_status'], relative['share_status'], relative['first_name'], relative['last_name'], profile_id, relative['match_id'] 
        else:
            pass

    elapsed_time = time() - t     # how many seconds it took        
            
    #log.debug("account_id: %s name: %s" % (request.session["account_id"], request.session["name"]))
    #return redirect("/results")
    #print 'count of items printed', counter
    return HttpResponse('Introductions sent: %s not sent: %s in %s seconds; total count: %s' % ( counter, not_counter, elapsed_time, total_count))

def _update_text(text, name):
    #replace **name** with name if it exists, or Cousin
    if name == None:
        text = text.replace('**name**', 'Cousin')
    else:
        text = text.replace('**name**', name)    
    return text
               
def _get_profile_choices(request):
    c = api.client.OAuthClient(request.session[api.client.OAUTH_KEY])
    names = c.get_name_profile()    
    choices = []
    for profile in json.loads(names)['profiles']:
        choices.append([profile['id'], '%s %s' % (profile['first_name'], profile['last_name'])])
    return choices
def _test_intro_relatives(request, profile_id, match_id):
    c = api.client.OAuthClient(request.session[api.client.OAUTH_KEY])
    # log the json from the profile_id and match_id from the get_relatives function
    log.debug('_test get relative %s ' % json.loads(c.get_relatives(profile_id, match_id)))
    # the next function will log the get introduction json
    c.get_send_status(profile_id, match_id)
    

    
