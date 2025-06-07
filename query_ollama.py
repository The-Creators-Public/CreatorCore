from ollama import chat
from ollama import ChatResponse

# Store conversation history per user or session
conversation_histories = {}

async def query_ollama(prompt: str, session_id: str = "default") -> str:
    try:
        with open(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\instructions.txt", "r", encoding="utf-8") as f:
            instructions = f.read()

        # Initialize history if not present
        if session_id not in conversation_histories:
            conversation_histories[session_id] = [
                {"role": "system", "content": instructions}
            ]

        # Append user prompt to history
        conversation_histories[session_id].append({"role": "user", "content": prompt})

        # Send full conversation history to Ollama API
        response: ChatResponse = chat(model="llama3.2", messages=conversation_histories[session_id])

        # Append assistant response to history
        conversation_histories[session_id].append({"role": "assistant", "content": response.message.content})

        return response.message.content  # type: ignore
    except Exception as e:
        return f"Error: Failed to get response from Ollama. {str(e)}"
