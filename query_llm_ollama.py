from ollama import chat
from ollama import ChatResponse

async def query_ollama(prompt: str) -> str:
    try:
        with open(r"C:\Users\angie\The Creators Public\creatorcore-bot\instructions.txt", "r", encoding="utf-8") as f:
            instructions = f.read()
        response: ChatResponse = chat(model="llama3.2", messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt},
        ])
        return response.message.content # type: ignore
    except Exception as e:
        return f"Error: Failed to get response from Ollama. {str(e)}"
