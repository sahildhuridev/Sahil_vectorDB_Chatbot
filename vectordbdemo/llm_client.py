import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Initialize client variable
client = None

def init_llm():
    """Configures the OpenRouter client using the API key."""
    global client
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        return True
    return False

def ask_llm(prompt: str) -> str:
    """Sends a prompt to OpenRouter and returns the generated text."""
    global client
    
    # Initialize if not already done
    if client is None:
        if not init_llm():
            return "Error: OPENROUTER_API_KEY environment variable is not set."
            
    try:
        # Defaulting to Gemini 2.0 Flash via OpenRouter as it's efficient
        # You can change this to any supported OpenRouter model string
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            return "I'm sorry, I couldn't generate a proper response."
    except Exception as e:
        return f"Error communicating with OpenRouter: {str(e)}"
