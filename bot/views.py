from django.shortcuts import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json 
import helpers 

SLACK_BOT_OAUTH_TOKEN = helpers.config("SLACK_BOT_OAUTH_TOKEN", default=None, cast=str)

# Create your views here.


def send_message(message, channel_id=None):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset-utf8",
        "Authorization": f"Bearer {SLACK_BOT_OAUTH_TOKEN}",
        "Accept": "application/json" 
    }
    data = {
        "channel": f"{channel_id}",
        "text": message
    }
    return requests.post(url,json=data, headers=headers)


@csrf_exempt
@require_POST
def slack_event_endpoints(request):
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except:
        pass 
    data_type = json_data.get('type')
    print(data_type, json_data.keys(),json_data)
    allowed_data_type = [
        'event_callback',
        'url_verification'
    ]
    if data_type not in allowed_data_type:
        return HttpResponse("Not Allowed", status=400)
    if data_type == "url_verification":
        challenge = json_data.get('challenge')
        if challenge is None:
            return HttpResponse("Not Allowed", status=400) 
        return HttpResponse(challenge,status=200)
    return HttpResponse("Success",status=200)