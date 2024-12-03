from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def slack_event_endpoints(request):
    print(request.body, request.method)
    return HttpResponse("<h1>Hello I am Pritam, Welcome World</h1>",status=200)


# https://api.slack.com/apps/A082KQNFLE6/event-subscriptions?