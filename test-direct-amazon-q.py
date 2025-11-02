#!/usr/bin/env python3
"""
Direct test of Amazon Q with the exact context that would be sent
"""

import subprocess
import sys
import os

# Add current directory to import the chat function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def clean_ansi_codes(text: str) -> str:
    """Remove ANSI color codes and formatting from text"""
    import re
    # Remove ANSI escape sequences
    cleaned = re.sub(r'\x1b\[[0-9;]*m', '', text)
    cleaned = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', cleaned)
    cleaned = re.sub(r'\[[\d;]+m', '', cleaned)
    cleaned = re.sub(r'\[\d+m', '', cleaned)
    
    # Clean up extra whitespace and newlines
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

def chat_with_amazon_q_debug(message: str, context: str = "") -> tuple[bool, str]:
    """Test version of chat_with_amazon_q with debug output"""
    try:
        print(f"🔍 DEBUG: chat_with_amazon_q() called")
        print(f"🔍 DEBUG: Message: {message[:100]}...")
        print(f"🔍 DEBUG: Context length: {len(context)} chars")
        print(f"🔍 DEBUG: Context preview: {context[:300]}...")
        
        # Combine context and message
        full_prompt = f"{context}\n\nUser Question: {message}" if context else message
        print(f"🔍 DEBUG: Full prompt length: {len(full_prompt)} chars")
        print(f"🔍 DEBUG: Full prompt:")
        print("=" * 80)
        print(full_prompt)
        print("=" * 80)
        
        # Call Amazon Q CLI
        print(f"🔍 DEBUG: Calling Amazon Q CLI with subprocess.run()")
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=60)
        print(f"🔍 DEBUG: Amazon Q CLI returned with code: {result.returncode}")
        
        if result.returncode == 0:
            raw_output = result.stdout.strip()
            print(f"🔍 DEBUG: Raw output length: {len(raw_output)} chars")
            print(f"🔍 DEBUG: Raw output:")
            print("-" * 80)
            print(raw_output)
            print("-" * 80)
            
            clean_output = clean_ansi_codes(raw_output)
            print(f"🔍 DEBUG: Clean output length: {len(clean_output)} chars")
            
            if clean_output:
                print(f"🔍 DEBUG: Returning SUCCESS with clean output")
                return True, clean_output
            else:
                print(f"🔍 DEBUG: Empty response after cleaning")
                return False, "Amazon Q returned an empty response"
        else:
            error_msg = result.stderr.strip()
            print(f"🔍 DEBUG: Error message: {error_msg}")
            
            if "not logged in" in error_msg.lower():
                print(f"🔍 DEBUG: Not logged in error detected")
                return False, "Authentication required. Please login to Amazon Q CLI."
            else:
                print(f"🔍 DEBUG: Other error detected")
                return False, f"Amazon Q error: {clean_ansi_codes(error_msg)}"
                
    except subprocess.TimeoutExpired:
        print(f"🔍 DEBUG: Amazon Q CLI chat request timed out")
        return False, "Request timed out. Please try again with a shorter message."
    except Exception as e:
        print(f"🔍 DEBUG: Error in Amazon Q chat: {str(e)}")
        return False, f"Error in Amazon Q chat: {str(e)}"

def test_exact_workflow():
    """Test the exact workflow that happens in the app"""
    
    print("🚀 Testing Exact CHI Analyzer Workflow")
    print("=" * 80)
    
    # Exact analysis data that would be used
    analysis_data = {
        'exit_from_red': 5,
        'return_back_red': 3,
        'new_comer_red': 2,
        'missing_from_chi': 1,
        'total_customers': 11,
        'low_score_improvement_pct': 18.2
    }
    
    # Exact AI summary that would be generated
    ai_summary = """# CHI Security Analysis Summary

## Key Findings
- **Exit from Red**: 5 customers improved their security scores
- **Return Back to Red**: 3 customers deteriorated  
- **New Comer to Red**: 2 new customers with low scores
- **Missing from CHI**: 1 customers without data

## Overall Assessment
The security posture shows a 18.2% improvement this month."""
    
    # Exact context that would be generated
    context = f"""
        Current CHI Analysis Data:
        - Exit from Red: {analysis_data['exit_from_red']} customers
        - Return Back to Red: {analysis_data['return_back_red']} customers  
        - New Comer to Red: {analysis_data['new_comer_red']} customers
        - Missing from CHI: {analysis_data['missing_from_chi']} customers
        - Total customers: {analysis_data['total_customers']}
        - Improvement: {analysis_data['low_score_improvement_pct']:.1f}%
        
        Current AI Summary (this is what the user is currently seeing):
        {ai_summary}
        """
    
    # Exact question that would be asked
    question = "Please rewrite the summary to focus more on the positive improvements and success stories. Highlight the customers who improved their security scores."
    
    print("📋 Test Parameters:")
    print(f"- Analysis data: {analysis_data}")
    print(f"- AI summary length: {len(ai_summary)} chars")
    print(f"- Context length: {len(context)} chars")
    print(f"- Question: {question}")
    print()
    
    # Call Amazon Q with exact parameters
    success, response = chat_with_amazon_q_debug(question, context)
    
    print("\n📊 Test Results:")
    print(f"- Success: {success}")
    print(f"- Response length: {len(response) if response else 0} chars")
    
    if success:
        print("\n✅ SUCCESS! Amazon Q responded correctly.")
        print("This proves the workflow should work in the actual app.")
        print("\nResponse preview:")
        print("-" * 40)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 40)
    else:
        print(f"\n❌ FAILED: {response}")
        print("This explains why the app isn't working.")
    
    return success, response

if __name__ == "__main__":
    test_exact_workflow()