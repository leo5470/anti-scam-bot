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
    PushMessageRequest,
    GroupSummaryResponse,
    TextMessage,
    TemplateMessage,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent,
    JoinEvent
)

# from openaiFunc import query_openai
from vertexAI import query_vertexAI
from mongo import MongoDBClient

import os
from pathlib import Path

# If you need to run from local (ngrok or others), uncomment the following 2 lines.
# from dotenv import load_dotenv
# load_dotenv()

client = MongoDBClient()

app = Flask(__name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

binaryPrompt = Path('./prompts/binary.txt').read_text()
qaPrompt = Path('./prompts/qa.txt').read_text()
suggestPrompt = Path('./prompts/suggest.txt').read_text()

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

@handler.add(FollowEvent)
def handle_add_friend(event):
    userID = event.source.user_id
    client.newUser(userID)

@handler.add(JoinEvent)
def handle_join_group(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        groupID = event.source.group_id
        group_summary = line_bot_api.get_group_summary(groupID).to_dict()
        groupName = group_summary["groupName"]
        client.insertGroup(groupID, groupName)



@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        incomingMessage = event.message.text
        userID = event.source.user_id
        if(event.source.type == "group"):
            groupID = event.source.group_id
            init = client.initializeGroup(userID, groupID, incomingMessage)
            if init:
                messages = [TextMessage(text="初始化成功")]
            else:
                client.updateGroupHistory(userID, groupID, incomingMessage)
                history = client.getGroupHistory(groupID=groupID, groupName=None)
                resp = query_vertexAI(binaryPrompt, history, temperature=0)
                if resp == "是":
                    caution = "⚠️ 警告! 警告! 以上內容有點危險喔，可以點選選單內的”我該怎麼做”馬上了解下一步該做甚麼" # TODO: 警告訊息
                    messages = [TextMessage(text=caution)]
                    line_bot_api.push_message(
                        PushMessageRequest(to=userID, messages=messages)
                    )
                return
            

        elif incomingMessage == "/提示":
            groupNames = client.getGroupsInfo(userID)

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
            client.setSuggestFlag(userID, True)
        elif client.getSuggestFlag(userID):
                groupName = incomingMessage
                history = client.getGroupHistory(groupName=groupName)
                if history == None:
                    ans = "找不到指定群組，請再試一次！"
                    messages = [TextMessage(text=ans)]
                else:
                    ans = query_vertexAI(suggestPrompt, history)
                    if ans == "":
                        ans = "出了一點問題，導致無法輸出內容。也有可能是訊息還太短，導致無法生成，可以再試一次。"
                        messages = [TextMessage(text=ans)]
                    else:
                        client.updateSuggestHistory(userID, ans)
                        columns = [
                            CarouselColumn(
                                thumbnail_image_url='https://cdn.prod.website-files.com/6030eb20edb267a2d11d31f6/63bd0e73eda88718096a822c_ConceptsLINEGroupCoverImage_a76a181134deb7c405b39e6803a648c8_2000.png',
                                text="有關於提示的任何問題，可以按下面的「進行詢問」開始詢問！",
                                default_action=MessageAction(
                                        label="進行詢問", # TODO: change
                                        text="/詢問"
                                    ),
                                actions=[
                                    MessageAction(
                                        label="進行詢問", # TODO: change
                                        text="/詢問"
                                    ),
                                ]
                            )
                        ]
                        template = CarouselTemplate(columns=columns)
                        messages = [TextMessage(text=ans), TemplateMessage(altText="Ask Suggestion", template=template)]
                client.setSuggestFlag(userID, False)
        elif incomingMessage == "/詢問":
            suggest = client.getLatestSuggest(userID)
            client.updateChatHistory(userID, user=None, assistant=suggest)
            ans = "請開始詢問"
            messages = [TextMessage(text=ans)]
        elif incomingMessage == "/清空":
            client.clearChatHistory(userID)
            ans = "清空聊天記錄完畢！"
            messages = [TextMessage(text=ans)]
        else:
            client.updateChatHistory(userID, user=incomingMessage, assistant=None)
            history = client.getChatHistory(userID)
            ans = query_vertexAI(qaPrompt, history)
            if ans == "":
                ans = "出了一點問題，導致無法輸出內容。也有可能是訊息太短，可以在加長後再試一次。"
            else:
                client.updateChatHistory(userID, user=None, assistant=ans)
            messages = [TextMessage(text=ans)]
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")