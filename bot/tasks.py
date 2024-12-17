from celery import shared_task
import slacky
from . import utils

@shared_task
def slack_message_task(message, channel_id=None, user_id=None, thread_ts=None):
    gemini_message = utils.gemini_response(message)
    r = slacky.send_message(gemini_message, channel_id=channel_id, user_id=user_id, thread_ts=thread_ts)
    return r.status_code
