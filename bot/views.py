from django.shortcuts import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json 
import helpers 
from pprint import pprint

SLACK_BOT_OAUTH_TOKEN = helpers.config("SLACK_BOT_OAUTH_TOKEN", default=None, cast=str)

# Create your views here.


def send_message(message, channel_id=None, user_id=None):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset-utf8",
        "Authorization": f"Bearer {SLACK_BOT_OAUTH_TOKEN}",
        "Accept": "application/json" 
    }
    if user_id is not None:
        message = f"<@{user_id}>{message}" 
    data = {
        "channel": f"{channel_id}",
        "text": f"{message}".strip() 
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
    # print("\nData Type:",data_type,"\nJSON Keys:", json_data.keys(),"\nJSON Data:",json_data)
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
    elif data_type == "event_callback":
        event = json_data.get('event') or {}
        pprint(event)
        try:
            msg_text = msg_text = event['blocks'][0]['elements'][0]['elements'][1]['text']
        except:
            msg_text = event.get('text')
        user_id = event.get('user')
        channel_id = event.get('channel')
        r = send_message(message=msg_text, channel_id=channel_id, user_id=user_id)
        return HttpResponse("Success", status=r.status_code)
    return HttpResponse("Success",status=200)

# @csrf_exempt 
# @require_POST
# def slack_event_endpoints(request):
#     json_data = {}
#     try:
#         json_data = json.loads(request.body.decode('utf-8'))
#         print(json_data)
#     except Exception as e:
#         print(e)
#     data_type = json_data.get('type')
#     if data_type != "url_verification":
#             return HttpResponse("Not Allowed", status=400)
#     challenge = json_data.get('challenge') 
#     if challenge is None:
#         return HttpResponse("Not Allowed", status=400)
#     return HttpResponse(challenge, status=200) 