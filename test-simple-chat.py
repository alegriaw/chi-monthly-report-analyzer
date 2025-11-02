#!/usr/bin/env python3
"""
Simple test to verify Amazon Q chat functionality
"""

import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_amazon_q_chat():
    """Test Amazon Q chat with a simple message"""
    
    message = "Hello, please respond with a simple greeting."
    context = """
    Test Context:
    - This is a test message
    - Please respond briefly
    """
    
    full_prompt = f"{context}\n\nUser Question: {message}"
    
    print("🧪 Testing Amazon Q Chat")
    print(f"Full prompt:\n{full_prompt}")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=30)
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Chat successful!")
            return True, result.stdout.strip()
        else:
            print("❌ Chat failed!")
            return False, result.stderr.strip()
            
    except subprocess.TimeoutExpired:
        print("❌ Chat timed out!")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)

if __name__ == "__main__":
    success, response = test_amazon_q_chat()
    print(f"\nResult: {success}")
    print(f"Response: {response}")