#!/usr/bin/env python3
"""
Setup script for OpenRouter API configuration
"""

import os
import sys
from config import QWEN_CONFIG

def setup_openrouter():
    """Interactive setup for OpenRouter API"""
    print("Qwen2.5 VL 32B Setup for TAM Agent")
    print("=" * 40)
    
    print("Using Qwen2.5 VL 32B Instruct (Free Model)")
    print(f"Model: {QWEN_CONFIG['model']}")
    print(f"Base URL: {QWEN_CONFIG['base_url']}")
    
 
    if QWEN_CONFIG['api_key'] and QWEN_CONFIG['api_key'] != 'YOUR_OPENROUTER_API_KEY_HERE':
        print(f"\n✅ API key already configured")
        
      
        test_connection = input("\nTest connection now? (y/n): ").strip().lower()
        if test_connection == 'y':
            test_openrouter_connection(QWEN_CONFIG['api_key'])
    else:
        print("\n❌ API key not configured")
        print("Please edit config.py and set your OpenRouter API key")
        print("Get your API key from: https://openrouter.ai/")

def test_openrouter_connection(api_key):
    """Test OpenRouter API connection"""
    import requests
    
    print("\nTesting OpenRouter connection...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
  
    payload = {
        "model": "qwen/qwen-2.5-vl-32b-instruct",
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
            print("✅ Connection successful!")
            result = response.json()
            print(f"Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ Connection failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def show_usage():
    """Show usage examples"""
    print("\nUsage Examples:")
    print("=" * 20)
    
    print("\n1. Run a single test:")
    print("   python run_tam_tests.py --company 'A fintech startup'")
    
    print("\n2. Run comprehensive test:")
    print("   python run_tam_tests.py --all-companies")
    
    print("\n3. Run with verbose output:")
    print("   python run_tam_tests.py --verbose")
    
    print("\n4. Save results to file:")
    print("   python run_tam_tests.py --output results.json")

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_usage()
        return
    
    setup_openrouter()
    show_usage()

if __name__ == "__main__":
    main()
