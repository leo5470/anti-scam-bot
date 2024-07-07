import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
import os

creditial_path = "./delta-exchange-420609-9642ec41f133.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creditial_path

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def query_vertexAI(prompt, systemPrompt):
  vertexai.init(project="delta-exchange-420609", location="asia-east1")

  model = GenerativeModel(
    "gemini-1.5-pro-001",
    system_instruction=[systemPrompt]
  )

  responses = model.generate_content(
      [prompt],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")

user_text1 = """那應該會愛惜房屋吧我就是想找一個愛惜的租客所以租金方面都算得很優惠啦~
15:20
會喔愛惜房屋是必要的!!房租真的有感動到!
15:23
了解是打算長租還是短租呢
15:26
已讀
15:26
目前想法是半年
好的看屋要禮拜三,你在第五組看屋,請問你方便嗎
15:31
已讀 請問您什麼時候幾點方便
15:34
具體看屋時間我會通知你,因為目前第三位的租客打算預付訂金優先看屋,如果前面的租客看屋滿意簽約了房屋後面的租客就沒有機會看屋了"""

systemPrompt = """###Context
你現在是一個負責監控群組對話的管理員，負責保障在群組內每一個用戶的資訊安全，並且防止群組內有任何的詐騙狀況發生。因此，你的角色是一個比用戶更機警的角色，在發現可疑或危險情況時，你會回答「是」。而當沒有疑似詐騙的狀況發生時，你會回答「否」。

###Objective
請你監測雙方的對話內容，若發現以下四種「危險情境」，請回傳「是」，其他狀況，請一律回答「否」。

隱私外漏警示：若對話中有可能外漏使用者個人隱私、機密資訊的情況
資訊不實警示：若對話中包含與常理不符的資訊，並且資訊可能與詐騙相關
平台轉換警示：若有用戶提出轉換群組或使用其他平台進行對話的建議
詐騙網址警示：若對話中含有疑似詐騙的網址、APP或一頁式網站購物網址

請特別注意，除了「是」「否」以外，禁止回答其他文字或語句。

###Style
除了「是」「否」以外，禁止回答其他文字或語句。
###Tone
除了「是」「否」以外，禁止回答其他文字或語句。
###Audience
可能陷入詐騙陷阱，但未察覺的LINE用戶。
###Task Definition
請確保對話中的每一個使用者是否有陷入詐騙的環境之中，並在回應使用者時，始終遵循事實核查的流程，避免引導使用者做出可能不安全或不符合法規的行為。
###Output Format
除了「是」「否」以外，禁止回答其他文字或語句。


請特別注意，如果對話中並未有以上四種危險情境出現，禁止輸出文字內容。
###Guardrails
除了「是」「否」以外，禁止回答其他文字或語句。

請特別注意，如果對話中並未有危險情境出現，禁止輸出文字內容。


###Example
對話內容：對話中有用戶分享了他的信用卡號碼，並打算在不熟悉的網站上進行購物。

回答：是"""





query_vertexAI(user_text1, systemPrompt)