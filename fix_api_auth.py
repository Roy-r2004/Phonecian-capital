#!/usr/bin/env python3
"""
Script to help fix OpenRouter API authentication issues
"""

import requests
import json
from config import QWEN_CONFIG

def test_current_api_key():
    """Test the current API key from config.py"""
    print("Testing current API key from config.py...")
    print(f"API Key: {QWEN_CONFIG['api_key'][:20]}...")
    
    headers = {
        "Authorization": f"Bearer {QWEN_CONFIG['api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen/qwen2.5-vl-32b-instruct:free",
        "messages": [{"role": "user", "content": "Hello, this is a test."}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Current API key is working!")
            result = response.json()
            print(f"Response: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API key failed: {response.status_code}")
            try:
                error_json = response.json()
                print(f"Error: {error_json}")
            except:
                print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def get_new_api_key_instructions():
    """Provide instructions for getting a new API key"""
    print("\n" + "="*60)
    print("HOW TO GET A NEW OPENROUTER API KEY")
    print("="*60)
    print("1. Go to: https://openrouter.ai/")
    print("2. Sign up or log in to your account")
    print("3. Navigate to 'API Keys' in your dashboard")
    print("4. Click 'Create Key'")
    print("5. Copy the new API key")
    print("6. Update the 'api_key' field in config.py")
    print("\nThe API key should look like: sk-or-v1-...")
    print("="*60)

def update_config_file(new_api_key):
    """Update the config.py file with a new API key"""
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the API key in OPENROUTER_CONFIG
        old_key = QWEN_CONFIG['api_key']
        content = content.replace(old_key, new_api_key)
        
        # Write back to file
        with open('config.py', 'w') as f:
            f.write(content)
        
        print(f"✅ Updated config.py with new API key")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False

def main():
    """Main function"""
    print("OpenRouter API Authentication Fix Tool")
    print("="*50)
    
    # Test current API key
    if test_current_api_key():
        print("\n✅ Your API key is working correctly!")
        print("The issue might be elsewhere. Check your internet connection and try again.")
        return
    
    print("\n❌ Current API key is not working.")
    
    # Provide instructions
    get_new_api_key_instructions()
    
    # Ask user for new API key
    print("\nEnter your new OpenRouter API key (or press Enter to skip):")
    new_key = input().strip()
    
    if new_key and new_key.startswith('sk-or-v1-'):
        if update_config_file(new_key):
            print("\nTesting new API key...")
            # Re-import config to get updated key
            import importlib
            import config
            importlib.reload(config)
            
            # Test the new key
            headers = {
                "Authorization": f"Bearer {new_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "qwen/qwen2.5-vl-32b-instruct:free",
                "messages": [{"role": "user", "content": "Hello, this is a test."}],
                "max_tokens": 10
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ New API key is working!")
                    print("You can now run your TAM agent successfully.")
                else:
                    print(f"❌ New API key also failed: {response.status_code}")
                    print("Please check your OpenRouter account status and billing.")
                    
            except Exception as e:
                print(f"❌ Error testing new key: {e}")
    else:
        print("No valid API key provided. Please update config.py manually.")

if __name__ == "__main__":
    main()
