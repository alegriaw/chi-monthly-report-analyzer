#!/usr/bin/env python3
"""
Test script to verify session state handling in CHI Analyzer
"""

import streamlit as st

def test_session_state_persistence():
    """Test that session state persists across button clicks"""
    
    st.title("🧪 Session State Test")
    
    # Initialize test data
    if "test_ai_summary" not in st.session_state:
        st.session_state.test_ai_summary = "Original AI Summary - This should not reset when buttons are clicked"
    
    if "test_chat_history" not in st.session_state:
        st.session_state.test_chat_history = []
    
    if "pending_quick_question" not in st.session_state:
        st.session_state.pending_quick_question = None
    
    # Display current state
    st.subheader("Current State")
    st.write(f"AI Summary: {st.session_state.test_ai_summary}")
    st.write(f"Chat History Length: {len(st.session_state.test_chat_history)}")
    st.write(f"Pending Question: {st.session_state.pending_quick_question}")
    
    # Test buttons
    st.subheader("Test Buttons")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Test Focus", key="test_focus"):
            st.session_state.pending_quick_question = "Focus on improvements test"
            st.rerun()
    
    with col2:
        if st.button("⚠️ Test Risks", key="test_risks"):
            st.session_state.pending_quick_question = "Highlight risks test"
            st.rerun()
    
    with col3:
        if st.button("📊 Test Metrics", key="test_metrics"):
            st.session_state.pending_quick_question = "Add metrics test"
            st.rerun()
    
    # Handle pending question
    if st.session_state.pending_quick_question:
        question = st.session_state.pending_quick_question
        st.session_state.pending_quick_question = None
        
        # Simulate chat response
        response = f"Mock response to: {question}"
        st.session_state.test_chat_history.append((question, response))
        
        st.success(f"✅ Processed: {question}")
        st.info(f"Response: {response}")
    
    # Display chat history
    if st.session_state.test_chat_history:
        st.subheader("Chat History")
        for i, (q, r) in enumerate(st.session_state.test_chat_history):
            with st.expander(f"Chat {i+1}: {q[:30]}..."):
                st.write(f"Q: {q}")
                st.write(f"A: {r}")
    
    # Reset button
    if st.button("🗑️ Reset Test", key="reset_test"):
        st.session_state.test_ai_summary = "Original AI Summary - This should not reset when buttons are clicked"
        st.session_state.test_chat_history = []
        st.session_state.pending_quick_question = None
        st.success("✅ Test state reset")
        st.rerun()

if __name__ == "__main__":
    test_session_state_persistence()