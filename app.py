from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ['channel_access_token'])
# Channel Secret
handler = WebhookHandler(os.environ['channel_secret'])

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    if event.message.text == "哼!":
        message = TextSendMessage(text="哼哼!")
    elif event.message.text == "哎呀~":
        message = TextSendMessage(text="哎呀呀~")
    elif event.message.text == "嘿嘿~":
        message = TextSendMessage(text="嘿嘿嘿~")
    elif event.message.text == "謝謝~":
        message = TextSendMessage(text="不謝~")
    elif event.message.text == "厲害了!!":
        message = TextSendMessage(text="真的太厲害了!!")
    elif event.message.text == "氣哭":
        message = TextSendMessage(text="氣哭!!")
    else:
        message = TextSendMessage(text=event.message.text)

    line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def hello():
    # print(os.environ['channel_access_token'])
    # print(os.environ['channel_secret'])
    return 'Hello World!';

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# pip freeze > requirements.txt
# echo web: python app.py > Procfile
