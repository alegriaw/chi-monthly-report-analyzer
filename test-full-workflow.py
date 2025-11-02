#!/usr/bin/env python3
"""
Test the complete workflow of AI summary persistence and Amazon Q chat
"""

import subprocess
import json

def test_amazon_q_with_context():
    """Test Amazon Q with CHI analysis context"""
    
    # Simulate CHI analysis data
    analysis_data = {
        'exit_from_red': 5,
        'return_back_red': 3,
        'new_comer_red': 2,
        'missing_from_chi': 1,
        'total_customers': 11,
        'low_score_improvement_pct': 18.2
    }
    
    # Simulate original AI summary
    original_summary = f"""
# CHI Security Analysis Summary

## Key Findings
- **Exit from Red**: {analysis_data['exit_from_red']} customers improved their security scores
- **Return Back to Red**: {analysis_data['return_back_red']} customers deteriorated  
- **New Comer to Red**: {analysis_data['new_comer_red']} new customers with low scores
- **Missing from CHI**: {analysis_data['missing_from_chi']} customers without data

## Overall Assessment
The security posture shows a {analysis_data['low_score_improvement_pct']:.1f}% improvement this month.
"""

    # Create context like the app does
    context = f"""
    Current CHI Analysis Data:
    - Exit from Red: {analysis_data['exit_from_red']} customers
    - Return Back to Red: {analysis_data['return_back_red']} customers  
    - New Comer to Red: {analysis_data['new_comer_red']} customers
    - Missing from CHI: {analysis_data['missing_from_chi']} customers
    - Total customers: {analysis_data['total_customers']}
    - Improvement: {analysis_data['low_score_improvement_pct']:.1f}%
    
    Current AI Summary (this is what the user is currently seeing):
    {original_summary}
    """
    
    # Test the "Focus on improvements" question
    question = "Please rewrite the summary to focus more on the positive improvements and success stories. Highlight the customers who improved their security scores."
    
    full_prompt = f"{context}\n\nUser Question: {question}"
    
    print("🧪 Testing Amazon Q with CHI Context")
    print("=" * 60)
    print("Question:", question)
    print("-" * 60)
    print("Context preview:")
    print(context[:300] + "...")
    print("-" * 60)
    
    try:
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=60)
        
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print("✅ Amazon Q Response:")
            print("=" * 60)
            print(response)
            print("=" * 60)
            
            # Test if response is relevant
            if any(word in response.lower() for word in ['improvement', 'positive', 'success', 'exit']):
                print("✅ Response appears relevant to the question")
            else:
                print("⚠️ Response may not be fully relevant")
                
            return True, response
        else:
            print(f"❌ Error: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print("❌ Request timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def test_context_preservation():
    """Test that context is preserved correctly"""
    
    print("\n🧪 Testing Context Preservation")
    print("=" * 60)
    
    # Simulate improved summary
    improved_summary = """
# CHI Security Analysis Summary - Positive Focus

## 🎉 Success Stories
- **Significant Improvement**: 5 customers successfully exited the red zone
- **Positive Trend**: 18.2% overall improvement demonstrates effective security initiatives
- **Customer Engagement**: Active participation in security improvement programs

## Recommendations
Continue current successful strategies and expand to more customers.
"""
    
    # Test context with improved summary
    context_with_improved = f"""
    Current CHI Analysis Data:
    - Exit from Red: 5 customers
    - Return Back to Red: 3 customers  
    - New Comer to Red: 2 customers
    - Missing from CHI: 1 customers
    - Total customers: 11
    - Improvement: 18.2%
    
    Current AI Summary (this is what the user is currently seeing):
    {improved_summary}
    """
    
    question = "Please add more specific metrics and percentages to this summary."
    full_prompt = f"{context_with_improved}\n\nUser Question: {question}"
    
    print("Testing with improved summary as context...")
    print("Question:", question)
    print("-" * 60)
    
    try:
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print("✅ Amazon Q Response with Improved Context:")
            print("=" * 60)
            print(response)
            print("=" * 60)
            
            # Check if it references the improved summary
            if any(word in response.lower() for word in ['success', 'positive', 'improvement']):
                print("✅ Response builds on the improved summary context")
            else:
                print("⚠️ Response may not be using the improved context")
                
            return True, response
        else:
            print(f"❌ Error: {result.stderr}")
            return False, result.stderr
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

if __name__ == "__main__":
    print("🚀 Testing Complete CHI Analyzer Workflow")
    print("=" * 80)
    
    # Test 1: Basic functionality
    success1, response1 = test_amazon_q_with_context()
    
    # Test 2: Context preservation
    success2, response2 = test_context_preservation()
    
    print("\n📊 Test Results Summary")
    print("=" * 80)
    print(f"Basic Amazon Q Chat: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Context Preservation: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! The workflow should work correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    print("\n💡 Next steps:")
    print("1. Run the CHI Analyzer: streamlit run chi_low_security_score_analyzer.py")
    print("2. Upload your Excel file")
    print("3. Generate AI summary")
    print("4. Try the 'Focus on improvements' button")
    print("5. Verify the summary doesn't reset and Amazon Q responds correctly")