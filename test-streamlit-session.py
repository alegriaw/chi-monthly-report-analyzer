#!/usr/bin/env python3
"""
Test Streamlit session state behavior directly
"""

import sys
import os

# Mock Streamlit session state
class MockSessionState:
    def __init__(self):
        self._state = {}
    
    def get(self, key, default=None):
        return self._state.get(key, default)
    
    def __setitem__(self, key, value):
        self._state[key] = value
    
    def __getitem__(self, key):
        return self._state[key]
    
    def __contains__(self, key):
        return key in self._state
    
    def __delitem__(self, key):
        if key in self._state:
            del self._state[key]
    
    def keys(self):
        return self._state.keys()

def test_session_state_flow():
    """Test the exact session state flow"""
    
    print("🧪 Testing Streamlit Session State Flow")
    print("=" * 60)
    
    # Create mock session state
    session_state = MockSessionState()
    
    # Simulate analysis data
    analysis_data = {
        'exit_from_red': 5,
        'return_back_red': 3,
        'new_comer_red': 2,
        'missing_from_chi': 1,
        'total_customers': 11,
        'low_score_improvement_pct': 18.2
    }
    
    print("Step 1: Initial state (first run)")
    print("-" * 40)
    
    # Step 1: Generate AI summary (first run)
    if "original_ai_summary" not in session_state:
        print("🔍 DEBUG: Generating NEW AI summary...")
        ai_summary = """# CHI Security Analysis Summary

## Key Findings
- **Exit from Red**: 5 customers improved their security scores
- **Return Back to Red**: 3 customers deteriorated  
- **New Comer to Red**: 2 new customers with low scores
- **Missing from CHI**: 1 customers without data

## Overall Assessment
The security posture shows a 18.2% improvement this month."""
        
        session_state['original_ai_summary'] = ai_summary
        session_state['ai_summary_generated'] = True
        print(f"🔍 DEBUG: AI summary generated and cached. Length: {len(ai_summary)} chars")
    
    # Initialize other states
    if "chat_history" not in session_state:
        session_state['chat_history'] = []
        print("🔍 DEBUG: Initialized empty chat_history")
    
    if "pending_quick_question" not in session_state:
        session_state['pending_quick_question'] = None
        print("🔍 DEBUG: Initialized pending_quick_question as None")
    
    # Check display summary
    ai_summary = session_state['original_ai_summary']
    display_summary = session_state.get('improved_summary', ai_summary)
    print(f"🔍 DEBUG: Display summary length: {len(display_summary)} chars")
    print(f"🔍 DEBUG: Using improved: {'improved_summary' in session_state}")
    
    print(f"\nSession state keys: {list(session_state.keys())}")
    
    print("\nStep 2: Button click simulation")
    print("-" * 40)
    
    # Step 2: Simulate button click
    question = "Please rewrite the summary to focus more on the positive improvements and success stories."
    session_state['pending_quick_question'] = question
    print(f"🔍 DEBUG: BUTTON CLICKED - Focus on improvements")
    print(f"🔍 DEBUG: Set pending_quick_question: {question[:50]}...")
    
    print("\nStep 3: Process pending question (after rerun)")
    print("-" * 40)
    
    # Step 3: Process pending question (simulating after rerun)
    if session_state['pending_quick_question']:
        print(f"🔍 DEBUG: PROCESSING PENDING QUESTION")
        quick_question = session_state['pending_quick_question']
        print(f"🔍 DEBUG: Question: {quick_question[:50]}...")
        session_state['pending_quick_question'] = None
        print(f"🔍 DEBUG: Cleared pending_quick_question")
        
        # Generate context
        current_summary = session_state.get('improved_summary', session_state.get('original_ai_summary', ai_summary))
        print(f"🔍 DEBUG: Current summary for context: {len(current_summary)} chars")
        
        context = f"""
        Current CHI Analysis Data:
        - Exit from Red: {analysis_data['exit_from_red']} customers
        - Return Back to Red: {analysis_data['return_back_red']} customers  
        - New Comer to Red: {analysis_data['new_comer_red']} customers
        - Missing from CHI: {analysis_data['missing_from_chi']} customers
        - Total customers: {analysis_data['total_customers']}
        - Improvement: {analysis_data['low_score_improvement_pct']:.1f}%
        
        Current AI Summary (this is what the user is currently seeing):
        {current_summary}
        """
        
        print(f"🔍 DEBUG: Generated context length: {len(context)} chars")
        
        # Simulate successful Amazon Q response
        mock_response = """# CHI Security Analysis Summary - Success Focus

## 🎉 Outstanding Achievements
- **5 customers successfully improved** their security scores and exited red status
- **18.2% overall improvement** demonstrates strong positive momentum
- **Nearly half of all customers** (45%) showed security enhancements

## Success Stories
The majority of security changes this month were positive improvements, with 5 customers demonstrating significant progress in their security posture.

## Next Steps
Continue successful strategies while providing targeted support for the remaining at-risk customers."""
        
        # Add to chat history
        session_state['chat_history'].append((quick_question, mock_response))
        print(f"🔍 DEBUG: Added to chat history. Total items: {len(session_state['chat_history'])}")
        
        print("\nStep 4: User applies improved summary")
        print("-" * 40)
        
        # Step 4: User clicks "Use this as new summary"
        session_state['improved_summary'] = mock_response
        print(f"🔍 DEBUG: Set improved_summary, length: {len(mock_response)} chars")
        
        # Check new display summary
        new_display_summary = session_state.get('improved_summary', ai_summary)
        print(f"🔍 DEBUG: New display summary length: {len(new_display_summary)} chars")
        print(f"🔍 DEBUG: Now using improved: {'improved_summary' in session_state}")
        
        print("\nStep 5: Second improvement (based on improved summary)")
        print("-" * 40)
        
        # Step 5: Another improvement based on the improved summary
        second_question = "Please add more specific metrics and percentages."
        current_summary_for_second = session_state.get('improved_summary', session_state.get('original_ai_summary', ai_summary))
        
        print(f"🔍 DEBUG: Second improvement using summary length: {len(current_summary_for_second)} chars")
        print(f"🔍 DEBUG: Is using improved summary: {current_summary_for_second == session_state.get('improved_summary')}")
        
        second_context = f"""
        Current CHI Analysis Data:
        - Exit from Red: {analysis_data['exit_from_red']} customers
        - Return Back to Red: {analysis_data['return_back_red']} customers  
        - New Comer to Red: {analysis_data['new_comer_red']} customers
        - Missing from CHI: {analysis_data['missing_from_chi']} customers
        - Total customers: {analysis_data['total_customers']}
        - Improvement: {analysis_data['low_score_improvement_pct']:.1f}%
        
        Current AI Summary (this is what the user is currently seeing):
        {current_summary_for_second}
        """
        
        print(f"🔍 DEBUG: Second context includes improved summary: {'Success Focus' in second_context}")
        print(f"🔍 DEBUG: Second context length: {len(second_context)} chars")
    
    print(f"\nFinal session state keys: {list(session_state.keys())}")
    print("✅ Session state flow test completed!")
    
    return session_state

if __name__ == "__main__":
    final_state = test_session_state_flow()
    
    print("\n📊 Final State Summary:")
    print(f"- Original AI summary: {len(final_state.get('original_ai_summary', '')) > 0}")
    print(f"- Improved summary: {len(final_state.get('improved_summary', '')) > 0}")
    print(f"- Chat history items: {len(final_state.get('chat_history', []))}")
    print(f"- Pending question: {final_state.get('pending_quick_question')}")
    
    if 'improved_summary' in final_state:
        print(f"\n✅ SUCCESS: Improved summary exists and would be used for further improvements")
        print(f"Improved summary preview: {final_state['improved_summary'][:200]}...")
    else:
        print(f"\n❌ ISSUE: No improved summary found")