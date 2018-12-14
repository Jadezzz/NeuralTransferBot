import urllib.request
import subprocess
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

import json

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

def save_img(url):
    # Saves image from user url to ./content/input.jpg for further usage
    urllib.request.urlretrieve(url, "/var/www/NeuralTransferBot/content/input.jpg")
def send_website_template(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {
            "id": id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        {       
                            "title":"Project Github Page",
                            "subtitle":"Check out this repo for more details",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://github.com/Jadezzz/NeuralTransferBot",
                                "messenger_extensions": "TRUE",
                                "webview_height_ratio": "FULL"
                            }
                        }
                    ]
                }
            } 
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_welcome_template(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {
            "id": id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Welcome!",
                                "subtitle": "I can do Neural Style Transfer!",
                                "image_url": "https://i.imgur.com/8vAv1wT.jpg",
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "Start!",
                                        "payload": "Start!"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "Examples",
                                        "payload": "Examples"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "About",
                                        "payload": "About"
                                    }
                                ]
                            }
                        ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_img(id, path):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN) 
    r = open(path, 'rb')  
    data = {
        'recipient':json.dumps({
            'id':id
        }),
        'message':json.dumps({
            'attachment':{
                'type':'image', 
                'payload':{}
            }
        }),
        'filedata': (os.path.basename(path), r , 'image/jpeg')
    }
    
    multipart_data = MultipartEncoder(data)
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }
    response = requests.post(url, headers=multipart_header, data=multipart_data)

    r.close()

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_attachment(id, attachment_id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN) 
    payload = {
        "recipient": {
            "id": id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "attachment_id": attachment_id
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def get_image_id(num):
    if num == 1:
        return "2149646058697440"
    elif num == 2:
        return "2305373213042257"
    elif num == 3:
        return "516745915473247"
    elif num == 4:
        return "2026161817475017"
    elif num == 5:
        return "429747744224866"
    elif num == 6:  # ncku original image
        return "2270010073242931"
    elif num == 7:  # ncku transfered image
        return "434107690459930"
