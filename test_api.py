import anthropic
import os
from dotenv import load_dotenv

load_dotenv('.env')
api_key = os.getenv('ANTHROPIC_API_KEY')

print(f"API Key loaded: {api_key[:20]}..." if api_key else "❌ No API key found in .env")

if api_key:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=50,
            messages=[{'role': 'user', 'content': 'Say test'}]
        )
        print("✅ API KEY WORKS!")
        print(f"Response: {message.content[0].text}")
    except anthropic.AuthenticationError:
        print("❌ API key is INVALID or REVOKED")
    except anthropic.PermissionDeniedError:
        print("❌ API key lacks permissions")
    except Exception as e:
        print(f"❌ Error: {e}")
