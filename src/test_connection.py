"""
Test OpenAI API Connection 
"""

import sys
from openai import OpenAI
from config import validate_config, OPENAI_API_KEY, DEFAULT_MODEL

def test_openai_connection():
    """ basic OpenAI API call"""
    
    print(" Testing OpenAI API Connection...\n")
    
    # Validate config first
    if not validate_config():
        return False
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Simple test prompt
        print(" Sending test prompt to OpenAI..")
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": "Say 'Hello! I am ready to help with research.' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        # Extract response
        result = response.choices[0].message.content
        return True
        
    except Exception as e:
        print(f"\n Error: {str(e)}\n")
        if "authentication" in str(e).lower() or "api key" in str(e).lower():
            print(" Solution: Check your OPENAI_API_KEY in .env file")
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    sys.exit(0 if success else 1)