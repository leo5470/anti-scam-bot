from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://140.112.26.229:8000/v1/")


def query_openai(prompt, systemPrompt="你是一名幫助人類的助手", top_p=0.7, max_tokens=512, temperature=0.95):
    # api_key = os.environ['OPENAI_API_KEY']
    
    completion = client.chat.completions.create(
        model="yentinglin/Llama-3-Taiwan-8B-Instruct",
        messages = [
            {
                "role": "system",
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": prompt 
            }
        ],
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content