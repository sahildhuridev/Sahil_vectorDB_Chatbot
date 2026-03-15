import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_openrouter():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY is not found in your .env file.")
        return

    print(f"Key found: {api_key[:10]}...")
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        print("Connecting to OpenRouter...")
        
        model_name = "google/gemini-2.0-flash-001"
        print(f"Testing model: {model_name}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Say 'Hello! Your OpenRouter key is working!'"}
            ]
        )
        
        if response.choices and response.choices[0].message:
            print(f"✅ Success! Response: {response.choices[0].message.content}")
        else:
            print("⚠️ No text returned in response.")
            
    except Exception as e:
        print(f"❌ OpenRouter Error: {str(e)}")

if __name__ == "__main__":
    test_openrouter()
