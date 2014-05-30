from django.shortcuts import render_to_response

def home(request):
    #just calling home page
    #return render_to_response('members/profile.html', {'choices':choices},
    #               context_instance=RequestContext(request))
    return render_to_response('home/home.html')
