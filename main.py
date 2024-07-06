from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from openaiFunc import query_openai
import os

# the main entrypoint to use FastAPI.
app = FastAPI()


line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# 指定函數處理來自/路徑的 POST 請求。
# 使用 post 表示這個端點只接受HTTP POST方法的請
# 求，這是API通常接收數據的方式。
@app.post("/")
# callback功能：用來回應特定事件或請求。
async def callback(request: Request):
    # FastAPI框架，回傳一個包含整個請求text的bytes
    # await表示該方法可能需要一些時間完成，在此期間
    # 非同步運行能去做其他工作。
    body = await request.body() 
    body = body.decode()

    # request.headers是一個字典，包含了所有http header資訊，
    # .get('x-line-signature')嘗試獲取與x-line-signature相關的值。
    # 與LINE平台互動，x-line-signature是個非常重要的字段，它包含
    # 了一個簽名，她用於驗證請求確實是從LINE平台發送的，是一個安
    # 全措施，用於確保接收到的數據的真實性與完整性。
    x_line_signature = request.headers.get('x-line-signature')

    # 處理來自LINE平台的Webhook請求並進行安全性檢查。
    # try: 呼叫WebhookHandler的handle方法，該方法是
    # line-bot-sdk 提供的方法，用於處理Webhook事件。
    # handle 方法會使用 x_line_signature 來驗證 body 
    # 的數字簽名是否有效。這是為了確保請求是從LINE平台
    # 發出的，並且內容在傳輸過程中沒有被篡改。
    # except: HTTPException 是FastAPI提供的一種特殊異常，
    # 用於在HTTP請求中返回錯誤響應。這裡設置狀態碼為 403，
    # 表示服務器理解請求但拒絕執行，並且詳細說明為 "Invalid 
    # signature"，告知客戶端或開發者簽名驗證失敗的具體原因。 
    try:
        handler.handle(body, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=403, detail="Invalid signature")

    # 取得 reply token 和訊息
    # 等待request.json()非同步方法的完成。該方法將請求的text解析成字典。
    # 詳細解釋在test_json.py
    json_data = await request.json()
    reply_token = json_data['events'][0]['replyToken']
    user_message = json_data['events'][0]['message']['text']

    # 使用OpenAI GPT自動回覆
    gpt_response = query_openai(user_message)

    # 回應用戶訊息
    line_bot_api.reply_message(
        reply_token, # 指定回應發送到哪個對話
        TextSendMessage(text=gpt_response)
    )

    # 返回一個字典，表明請求已經被正確處理。在FastAPI中，這會自動被轉換為JSON格式的HTTP響應，返回給調用方。
    return {"message": "OK"}
