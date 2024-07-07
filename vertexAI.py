# 使用 Google 帳戶進行身份驗證
# 這個命令會啟動網頁瀏覽器，讓你登錄到你的 Google 帳戶並授權。授權後，會生成應用程序默認憑證，用於在程式中驗證和授權 Google Cloud API。
# TODO: 用ChatVertexAI 代替 gcloud login? 
# pip install --upgrade google-cloud-aiplatform'
# gcloud auth application-default login
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def query_vertexAI(system, user, temperature=1, max_output_tokens=8192, top_p=0.95):

  vertexai.init(project="delta-exchange-420609", location="asia-east1")

  model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=[system]
  )

  generation_config = {
    "max_output_tokens": max_output_tokens,
    "temperature": temperature,
    "top_p": top_p,
  }
  
  safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  }

  response = model.generate_content(
      [user],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=False,
  )

  print(response.text, end="")