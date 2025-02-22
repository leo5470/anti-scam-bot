# 反詐騙 Line Bot - 思辨機器人"你那個愛找碴的朋友"

SITCON Hackathon 2024 成果發表

> **公創新世代：學生力量與科技共創公民參與 & 對抗網路詐騙假訊息 X LINE**

## 競賽議題 & 子議題
- 團隊名稱：你說對就隊
- 成員姓名：鄭席鈞, 吳予淨, 邱文良, 謝昕達
- 競賽議題：公創新世代：學生力量與科技共創公民參與
    - 子議題：對抗網路詐騙假訊息

### 專案簡介
- 用途/功能："你那個愛找碴的朋友"，此bot可以預防針對Line平台1對1所發生的各類型詐騙以及檢測各種可疑的訊息，並同時在審核後提供民眾思考的新思路，有以下三個主要功能：
    - 安全審核：bot會在群組內監測雙方的對話內容，特別針對「隱私外漏」、「資訊不實」、「平台轉換」、「詐騙網址」進行警示，身為一個使用者更機警的角色，做到初步防範的機制。
    - 驗證機制：使用者將bot加入群組可以對使用者起到防禦的功能，不僅讓使用者在對話中可以獲得安全感，也可以讓對方知道自己正在被檢核中，從源頭降低詐騙成功的機率。
    - 後續步驟提供：在bot接收到聊天室訊息後，可以藉由分析聊天室訊息，藉由LLM做到引導跟提醒使用者的功能，我們也同時提供使用者目前公開資源的質量化參考資料，讓使用者可以更有效的了解對話議題。
    - 思路提供：使用者可能因為非專業學者以及對聊天議題領不夠深入，並協助使用者包裝他想問的問題，避免使用者因為對於話題本身的"不熟悉"以及不知道如何詢問對方而上當受騙。

- 目標客群&使用情境：
    - 使用情境：我們希望能將聊天所引起的詐騙，杜絕在詐騙方正在「獲取信任」的階段，藉由Vertex AI的LLM做到基礎判斷詐騙方所傳達的資訊是否符合常理，並且同時引起使用者的思考。
    - 目標客群：
        - 一般民眾：此bot所針對的客群為一般民眾，藉由串接Vertex AI與民眾對話幫助一般民眾做到驗證、審核、思考，藉由簡單的按鍵以及system prompts的設定
        - Line平台：我們希望針對在台灣最大的聊天平台中作為主要的使用情境，使用者可能習慣藉由社群、群組以及1對1的聊天獲得各種資訊。在平台中，可能參雜真真假假的資訊，而使用者無法時刻了解，在聊天中利用bot增加一個防範的機制，杜絕由聊天引起的詐騙。
### 試試看吧！
Powered by Render.

![image](https://github.com/leo5470/anti-scam-bot/assets/61446148/e204bce8-cb3e-4c98-a0ae-0a08857b4a8a)
     
        
### 如何部署
- 環境設置
  1. 先在LINE Developers 建立Providers -> Create a Messaging API channel，並且儲存等一下會用到的CHANNEL_ACCESS_TOKEN與CHANNEL_SECRERT。
    2. （雲端部署）在Render或其他部署工具上，將先前建立好的token，連同其他環境變數，填入環境變數中。
       ![image](https://hackmd.io/_uploads/Bkih5jDvC.png)
       （本地部署）將main.py中的dotenv部分取消註解，將環境變數填入.env後，配合ngrok或其他工具即可使用。
- 使用者操作方式<br>
        - 使用方法1:
            - 加入LINE官方帳號即可開始進行問答。
        - 使用方法2:
            - 先創立一個只有自己和機器人群組，再將需要1對1對話的陌生人加進去。

    
### 使用資源
- 企業資源：
    - 管理即時通訊應用程式的工具接口:LINE Messaging API<br>
    - 資料庫：MongoDB<br>
    - 部署工具：Render<br>
    - 選用模型:Vertex AI (Gemini Pro 1.5)<br>
### 範例
<img src="https://github.com/leo5470/anti-scam-bot/assets/61446148/a7f09a2f-d843-4837-a9e1-59a05a9e0857" alt="screenshot 1" width="200"/>
<img src="https://github.com/leo5470/anti-scam-bot/assets/61446148/90eef9ff-4ca7-4e03-b41e-6fb4dd8e3f5e" alt="screenshot 2" width="200"/>
<img src="https://github.com/leo5470/anti-scam-bot/assets/61446148/3dba7b9d-2f6f-427c-a65d-8abe04e78df1" alt="screenshot 3" width="200"/>

### 待辦事項
- [ ] 加入更多防呆機制
- [ ] 更多的 Exception Handling 及 型別檢查
- [ ] 將是/否的任務改為使用Gemini Flash 1.5


