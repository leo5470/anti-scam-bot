from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI(api_key="EMPTY", base_url="http://140.112.26.229:8000/v1/")


async def query_openai(systemPrompt, prompt, top_p=0.7, max_tokens=512, temperature=0.95):
    # api_key = os.environ['OPENAI_API_KEY']
    
    completion = await client.chat.completions.create(
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