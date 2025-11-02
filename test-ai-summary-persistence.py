#!/usr/bin/env python3
"""
Test script to verify AI summary persistence in CHI Analyzer
"""

import streamlit as st

def simulate_ai_summary_flow():
    """Simulate the AI summary generation and improvement flow"""
    
    st.title("🧪 AI Summary Persistence Test")
    
    # Simulate analysis data
    analysis_data = {
        'exit_from_red': 5,
        'return_back_red': 3,
        'new_comer_red': 2,
        'missing_from_chi': 1,
        'total_customers': 11,
        'low_score_improvement_pct': 18.2
    }
    
    # Step 1: Generate AI summary (only once)
    if "original_ai_summary" not in st.session_state:
        st.info("🤖 Generating AI summary...")
        # Simulate AI summary generation
        ai_summary = f"""
# CHI Security Analysis Summary

## Key Findings
- **Exit from Red**: {analysis_data['exit_from_red']} customers improved their security scores
- **Return Back to Red**: {analysis_data['return_back_red']} customers deteriorated
- **New Comer to Red**: {analysis_data['new_comer_red']} new customers with low scores
- **Missing from CHI**: {analysis_data['missing_from_chi']} customers without data

## Overall Assessment
The security posture shows a {analysis_data['low_score_improvement_pct']:.1f}% improvement this month.
        """
        st.session_state.original_ai_summary = ai_summary
        st.session_state.ai_summary_generated = True
        st.success("✅ AI summary generated and cached!")
    else:
        st.success("✅ Using cached AI summary")
    
    # Step 2: Display current summary
    ai_summary = st.session_state.original_ai_summary
    display_summary = st.session_state.get('improved_summary', ai_summary)
    
    # Show which summary is being displayed
    col_info, col_actions = st.columns([3, 1])
    
    with col_info:
        if 'improved_summary' in st.session_state:
            st.info("📝 **Showing improved summary** (modified by Amazon Q Chat)")
        else:
            st.info("📝 **Showing original AI summary**")
    
    with col_actions:
        if 'improved_summary' in st.session_state:
            if st.button("🔄 Revert", key="revert_summary"):
                del st.session_state.improved_summary
                st.success("✅ Reverted to original summary")
                st.rerun()
        
        if st.button("🔄 Regenerate", key="regenerate_summary"):
            if 'original_ai_summary' in st.session_state:
                del st.session_state.original_ai_summary
            if 'improved_summary' in st.session_state:
                del st.session_state.improved_summary
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = []
            st.success("✅ Regenerating AI summary...")
            st.rerun()
    
    # Display the summary
    st.markdown(display_summary)
    
    # Step 3: Chat improvement simulation
    st.markdown("---")
    st.subheader("💬 Improve Summary with Amazon Q Chat")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize pending question state
    if "pending_quick_question" not in st.session_state:
        st.session_state.pending_quick_question = None
    
    # Prepare context function
    def get_chat_context():
        current_summary = st.session_state.get('improved_summary', st.session_state.get('original_ai_summary', ''))
        return f"""
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
    
    # Display current context
    with st.expander("🔍 Current Context for Amazon Q"):
        st.text(get_chat_context())
    
    # Quick action buttons
    st.markdown("**Quick Actions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Focus on improvements", key="btn_improvements"):
            st.session_state.pending_quick_question = "Please rewrite the summary to focus more on the positive improvements and success stories."
            st.rerun()
    
    with col2:
        if st.button("⚠️ Highlight risks", key="btn_risks"):
            st.session_state.pending_quick_question = "Please rewrite the summary to emphasize the security risks and areas that need immediate attention."
            st.rerun()
    
    with col3:
        if st.button("📊 Add more metrics", key="btn_metrics"):
            st.session_state.pending_quick_question = "Please enhance the summary with more detailed metrics and statistical analysis."
            st.rerun()
    
    # Handle pending quick question
    if st.session_state.pending_quick_question:
        quick_question = st.session_state.pending_quick_question
        st.session_state.pending_quick_question = None
        
        st.info(f"🤖 Processing: {quick_question}")
        
        # Simulate Amazon Q response
        context = get_chat_context()
        
        if "focus.*improvements" in quick_question.lower():
            mock_response = """
# CHI Security Analysis Summary - Positive Focus

## 🎉 Success Stories
- **Significant Improvement**: 5 customers successfully exited the red zone, showing strong security posture enhancement
- **Positive Trend**: 18.2% overall improvement demonstrates effective security initiatives
- **Customer Engagement**: Active participation in security improvement programs

## Key Achievements
- Exit from Red: 5 customers (excellent progress!)
- Overall improvement rate: 18.2% (above target)
- Successful security implementations across multiple customer environments

## Recommendations
Continue current successful strategies and expand to more customers.
            """
        elif "risks" in quick_question.lower():
            mock_response = """
# CHI Security Analysis Summary - Risk Focus

## ⚠️ Critical Areas of Concern
- **Deteriorating Customers**: 3 customers returned to red zone - immediate attention required
- **New Risk Exposure**: 2 new customers identified with low security scores
- **Missing Data**: 1 customer without CHI data - potential blind spot

## Immediate Actions Required
1. Urgent intervention for 3 deteriorating customers
2. Onboarding support for 2 new low-score customers
3. Data collection for missing customer

## Risk Mitigation
Implement proactive monitoring and rapid response protocols.
            """
        else:
            mock_response = """
# CHI Security Analysis Summary - Enhanced Metrics

## 📊 Detailed Statistics
- **Exit from Red**: 5 customers (45.5% of total)
- **Return Back to Red**: 3 customers (27.3% of total)
- **New Comer to Red**: 2 customers (18.2% of total)
- **Missing from CHI**: 1 customer (9.1% of total)
- **Total customers**: 11
- **Net Improvement**: +18.2% (5 improved - 3 deteriorated = +2 net, 2/11 = 18.2%)

## Trend Analysis
- Improvement ratio: 5:3 (1.67:1 positive)
- Coverage rate: 90.9% (10/11 customers with data)
- Success rate: 45.5% of customers improved
            """
        
        # Add to chat history
        st.session_state.chat_history.append((quick_question, mock_response))
        
        # Display response
        st.success("✅ Response received!")
        st.markdown("**Amazon Q Response:**")
        st.markdown(mock_response)
        
        # Option to use as new summary
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Use this as new summary", key="replace_summary_quick"):
                st.session_state.improved_summary = mock_response
                st.success("✅ Summary updated! The new summary will be used in exports.")
                st.rerun()
        with col_b:
            if st.button("📋 Copy to clipboard", key="copy_quick"):
                st.success("✅ Response copied!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("**Chat History:**")
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
            with st.expander(f"💬 Chat {i+1}: {user_msg[:50]}..."):
                st.markdown(f"**You:** {user_msg}")
                st.markdown(f"**Amazon Q:** {ai_response}")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Debug information
    st.markdown("---")
    st.subheader("🔍 Debug Information")
    st.write("Session State Keys:", list(st.session_state.keys()))
    st.write("Original AI Summary Cached:", 'original_ai_summary' in st.session_state)
    st.write("Improved Summary Available:", 'improved_summary' in st.session_state)
    st.write("Chat History Length:", len(st.session_state.get('chat_history', [])))

if __name__ == "__main__":
    simulate_ai_summary_flow()