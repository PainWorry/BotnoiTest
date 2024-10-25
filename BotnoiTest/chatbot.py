# -*- coding: utf-8 -*-
"""Chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cHe2qzZk0BTsX_4DF4PO23S_HCY6ZWet
"""

pip install line-bot-sdk

!pip install flask-ngrok

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate,
    MessageAction, QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn
)

app = Flask(__name__)

# Initialize LINE API with your channel access token and secret
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text.lower()

    if user_message == "text":
        response = TextSendMessage(text="Hello, this is a text response!")
    elif user_message == "button":
        response = TemplateSendMessage(
            alt_text="Buttons Template",
            template=ButtonsTemplate(
                title="Choose an option",
                text="Please select",
                actions=[MessageAction(label="Option 1", text="Option 1"),
                         MessageAction(label="Option 2", text="Option 2")]
            )
        )
    elif user_message == "quick reply":
        response = TextSendMessage(
            text="Select an option",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=MessageAction(label="Choice 1", text="Choice 1")),
                       QuickReplyButton(action=MessageAction(label="Choice 2", text="Choice 2"))]
            )
        )
    elif user_message == "carousel":
        response = TemplateSendMessage(
            alt_text="Carousel Template",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title="Option 1", text="Description 1",
                        actions=[MessageAction(label="Choose", text="Option 1")]
                    ),
                    CarouselColumn(
                        title="Option 2", text="Description 2",
                        actions=[MessageAction(label="Choose", text="Option 2")]
                    )
                ]
            )
        )
    else:
        response = TextSendMessage(text="Type 'text', 'button', 'quick reply', or 'carousel'.")

    line_bot_api.reply_message(event.reply_token, response)

if __name__ == "__main__":
    app.run(port=5000)