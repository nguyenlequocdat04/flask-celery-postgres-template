import datetime as dt
import json
import requests

class SVC_Slack(object):

    def __init__(self, webhook_url, username="") -> None:
        self.webhook_url = webhook_url
        self.username = username


    def send_info_message(self, title, message):
        post_json = {
            "attachments": [
                {
                    "color": "#1264A3",
                    "title": f"INFO: {title}",
                    "text": message,
                    "ts": dt.datetime.now().timestamp()
                }
            ],
            'username': self.username,
            'link_names': 1
        }
        return requests.post(self.webhook_url, data=json.dumps(post_json), timeout=5)


    def send_warn_message(self, title, message):
        post_json = {
            "attachments": [
                {
                    "color": "#FCCC2D",
                    "title": f"WARN: {title}",
                    "text": message,
                    "ts": dt.datetime.now().timestamp()
                }
            ],
            'username': self.username,
            'link_names': 1
        }
        return requests.post(self.webhook_url, data=json.dumps(post_json), timeout=5)


    def send_error_message(self, title, message):
        post_json = {
            "attachments": [
                {
                    "color": "#e74c28",
                    "title": f"ERROR: {title}",
                    "text": message,
                    "ts": dt.datetime.now().timestamp()
                }
            ],
            'username': self.username,
            'link_names': 1
        }
        return requests.post(self.webhook_url, data=json.dumps(post_json), timeout=5)

