from evaluate import transfer
import my_utils
from fsm import MyMachine
from bottle import route, run, request, abort, static_file

VERIFY_TOKEN = "1234567890"



machine = MyMachine()

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)

@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    if body['object'] == 'page':
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
