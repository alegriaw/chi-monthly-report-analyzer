#!/usr/bin/env python3
"""
Test script for Amazon Q CLI status checking
"""

import subprocess
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_amazon_q_commands():
    """Test various Amazon Q CLI commands to find the fastest status check"""
    
    commands_to_test = [
        (['q', '--version'], "Version check"),
        (['q', 'login'], "Login status check"),
        (['q', 'chat', '--help'], "Chat help"),
        (['q', 'chat', 'hi'], "Simple chat test"),
    ]
    
    for cmd, description in commands_to_test:
        print(f"\n🧪 Testing: {description}")
        print(f"Command: {' '.join(cmd)}")
        
        start_time = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            duration = time.time() - start_time
            
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"📤 Return code: {result.returncode}")
            print(f"📝 Stdout: {result.stdout[:200]}...")
            print(f"❌ Stderr: {result.stderr[:200]}...")
            
            # Check for login indicators
            stderr_lower = result.stderr.lower()
            stdout_lower = result.stdout.lower()
            
            if "already logged in" in stderr_lower or "already logged in" in stdout_lower:
                print("✅ Status: Already logged in detected")
            elif "not logged in" in stderr_lower or "not logged in" in stdout_lower:
                print("❌ Status: Not logged in detected")
            elif result.returncode == 0:
                print("✅ Status: Command successful")
            else:
                print("⚠️  Status: Command failed")
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏱️  Duration: {duration:.2f}s (TIMEOUT)")
            print("❌ Status: Command timed out")
        except Exception as e:
            duration = time.time() - start_time
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"❌ Error: {e}")

def test_optimized_check():
    """Test the optimized Amazon Q availability check"""
    print("\n" + "="*50)
    print("🚀 Testing Optimized Amazon Q Status Check")
    print("="*50)
    
    start_time = time.time()
    
    try:
        # Step 1: Version check
        print("\n1️⃣ Checking version...")
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            print("❌ Amazon Q CLI not installed")
            return
        print(f"✅ Version: {version_result.stdout.strip()}")
        
        # Step 2: Login status check
        print("\n2️⃣ Checking login status...")
        login_check = subprocess.run(['q', 'login'], capture_output=True, text=True, timeout=5)
        stderr_lower = login_check.stderr.lower()
        stdout_lower = login_check.stdout.lower()
        
        if ("already logged in" in stderr_lower or "already logged in" in stdout_lower or
            "you are already authenticated" in stderr_lower or "you are already authenticated" in stdout_lower):
            print("✅ Already logged in detected")
            total_time = time.time() - start_time
            print(f"🎉 Total check time: {total_time:.2f}s")
            return
        
        # Step 3: Help command check
        print("\n3️⃣ Checking help command...")
        help_result = subprocess.run(['q', 'chat', '--help'], capture_output=True, text=True, timeout=3)
        if help_result.returncode == 0:
            print("✅ Help command works - assuming logged in")
            total_time = time.time() - start_time
            print(f"🎉 Total check time: {total_time:.2f}s")
            return
        else:
            if "not logged in" in help_result.stderr.lower():
                print("❌ Not logged in detected")
            else:
                print(f"⚠️  Help command failed: {help_result.stderr[:100]}")
        
        total_time = time.time() - start_time
        print(f"⏱️  Total check time: {total_time:.2f}s")
        
    except subprocess.TimeoutExpired as e:
        total_time = time.time() - start_time
        print(f"❌ Timeout after {total_time:.2f}s: {e}")
    except Exception as e:
        total_time = time.time() - start_time
        print(f"❌ Error after {total_time:.2f}s: {e}")

if __name__ == "__main__":
    print("🧪 Amazon Q CLI Status Test")
    print("="*50)
    
    # Test individual commands
    test_amazon_q_commands()
    
    # Test optimized approach
    test_optimized_check()
    
    print("\n✅ Test completed!")