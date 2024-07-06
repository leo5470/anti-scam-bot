from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from openaiFunc import query_openai

import os

app = Flask(__name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

suggestFlag = False

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        incoming = event.message.text

        if incoming == "\提示":
            groupNames = ["group 1", "group 2"]
            columns = [
                CarouselColumn(
                    thumbnail_image_url='https://cdn.prod.website-files.com/6030eb20edb267a2d11d31f6/63bd0e73eda88718096a822c_ConceptsLINEGroupCoverImage_a76a181134deb7c405b39e6803a648c8_2000.png',
                    text=name,
                    default_action=MessageAction(
                            label="選擇",
                            text=name
                        ),
                    actions=[
                        MessageAction(
                            label="選擇",
                            text=name
                        ),
                    ]
                )
                for name in groupNames
            ]
            template = CarouselTemplate(columns=columns)
            messages = [TemplateMessage(altText="Groups", template=template)]
            suggestFlag = True
        else: 
            if suggestFlag:
                history = "你正在接受測試"
                ans = query_openai(history) # TODO: change parameters
            else:
                ans = "請依照指示使用！"
            messages = [TextMessage(text=ans)]
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0")