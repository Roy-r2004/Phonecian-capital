#!/usr/bin/env python3
"""
Script to create Word documents with TAM and DCF responses
"""

from tam_qwen_agent import QwenTAMAgent
from dcf_agent import DCFAgent
from config import QWEN_CONFIG
from datetime import datetime
import os

def create_word_document(content, filename):
    """Create a simple text file that can be opened as a Word document"""
    try:
        # Create the file with .doc extension
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created document: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return False

def generate_tam_response():
    """Generate TAM response"""
    print("Generating TAM response...")
    agent = QwenTAMAgent(
        api_key=QWEN_CONFIG['api_key'],
        base_url=QWEN_CONFIG['base_url'],
        model=QWEN_CONFIG['model']
    )
    
    result = agent.test_prompt('A SaaS company providing project management software to small and medium businesses')
    return result.response

def generate_dcf_response():
    """Generate DCF response"""
    print("Generating DCF response...")
    agent = DCFAgent(
        api_key=QWEN_CONFIG['api_key'],
        base_url=QWEN_CONFIG['base_url'],
        model=QWEN_CONFIG['model']
    )
    
    result = agent.test_prompt('A SaaS company providing project management software to small and medium businesses')
    return result.response

def main():
    """Main function to create response documents"""
    print("Creating TAM and DCF Response Documents")
    print("=" * 50)
    
    # Generate TAM response
    try:
        tam_response = generate_tam_response()
        print(f"TAM response generated: {len(tam_response)} characters")
        
        # Create TAM response document
        tam_filename = r"C:\Phonecian Capital\Exercice 1\RESPONSE1_TAM_Roy Rizkallah_September 17.doc"
        create_word_document(tam_response, tam_filename)
        
    except Exception as e:
        print(f"❌ Error generating TAM response: {e}")
    
    # Generate DCF response
    try:
        dcf_response = generate_dcf_response()
        print(f"DCF response generated: {len(dcf_response)} characters")
        
        # Create DCF response document
        dcf_filename = r"C:\Phonecian Capital\Exercice 1\RESPONSE2_DCF_Roy Rizkallah_September 17.doc"
        create_word_document(dcf_response, dcf_filename)
        
    except Exception as e:
        print(f"❌ Error generating DCF response: {e}")
    
    print("\n✅ Response documents created successfully!")
    print("Files created:")
    print("- RESPONSE1_TAM_Roy Rizkallah_September 17.doc")
    print("- RESPONSE2_DCF_Roy Rizkallah_September 17.doc")

if __name__ == "__main__":
    main()
