# Debug Session State Tool

## Overview

The `debug-session-state.py` script is an advanced debugging tool designed to help developers and testers understand and validate session state behavior in the CHI Analyzer application. This interactive Streamlit application provides comprehensive insights into session state management, particularly for the AI chat functionality.

## Purpose

This debug tool addresses the critical need to:
- **Validate Session State Persistence**: Ensure that AI summaries and chat history persist correctly across user interactions
- **Test Without Dependencies**: Provide mock Amazon Q responses for testing without requiring CLI setup
- **Debug State Issues**: Identify and troubleshoot session state problems in a controlled environment
- **Validate Workflows**: Test the complete chat improvement workflow with realistic scenarios

## Key Features

### 1. Real-Time State Monitoring
- **Current Session State Display**: Shows all active session state variables and their values
- **State Change Tracking**: Monitors how session state changes with user interactions
- **Variable Inspection**: Detailed view of `original_ai_summary`, `improved_summary`, `chat_history`, and `pending_quick_question`
- **Enhanced Debug Output**: Improved debug logging with explicit output flushing for immediate visibility of button interactions and state changes

### 2. Mock Amazon Q Integration
- **No CLI Dependency**: Simulates Amazon Q responses without requiring actual CLI setup
- **Realistic Responses**: Generates contextually appropriate mock responses based on question type
- **Context Validation**: Shows exactly what context would be sent to Amazon Q
- **Response Processing**: Demonstrates how responses are processed and stored

### 3. Interactive Testing Interface
- **Quick Action Buttons**: Test the three main improvement scenarios:
  - 📈 **Focus on improvements**: Emphasizes positive trends and success stories (with enhanced debug output)
  - ⚠️ **Highlight risks**: Focuses on security risks and areas needing attention
  - 📊 **Add more metrics**: Enhances summary with detailed statistical analysis
- **Immediate Feedback**: Shows pending question status and processing flow with improved debug visibility
- **Response Options**: Allows testing of summary replacement workflow
- **Enhanced Debug Logging**: Real-time debug output with explicit flushing ensures immediate visibility of button clicks and state changes

### 4. Chat History Management
- **History Visualization**: Displays complete chat history with expandable entries
- **History Persistence**: Validates that chat history accumulates correctly
- **History Clearing**: Tests the chat history reset functionality

### 5. State Reset Capabilities
- **Complete Reset**: Clears all session state for fresh testing
- **Selective Reset**: Individual state variable management
- **State Recovery**: Tests application behavior after state loss

## Usage Instructions

### Starting the Debug Tool

```bash
# Activate your virtual environment
source chi_analyzer_env/bin/activate  # Linux/Mac
# or
chi_analyzer_env\Scripts\activate     # Windows

# Run the debug script
streamlit run debug-session-state.py
```

### Testing Workflow

#### 1. Initial State Inspection
- Launch the tool and observe the initial session state
- Note the automatically generated original AI summary
- Check that all required session state variables are initialized

#### 2. Quick Action Testing
- Click each quick action button (📈, ⚠️, 📊)
- Observe how pending questions are set and processed with enhanced debug output
- Verify that mock responses are generated appropriately
- Check that the original summary persists throughout
- Monitor console output for immediate debug feedback with explicit flushing

#### 3. Summary Replacement Testing
- After receiving a mock response, test the "Use this as new summary" functionality
- Verify that the improved summary is stored correctly
- Check that the display switches to show the improved version
- Confirm that the original summary is still preserved

#### 4. Chat History Validation
- Perform multiple quick actions to build chat history
- Verify that all conversations are stored and displayed
- Test the chat history clearing functionality
- Ensure history persists across different interactions

#### 5. Context Generation Testing
- Use the "Current Context" expander to view generated context
- Verify that the context includes the current summary (original or improved)
- Check that analysis data is properly formatted
- Ensure context changes appropriately when summary is improved

#### 6. State Reset Testing
- Use the "Reset All" button to clear all session state
- Verify that the application recovers gracefully
- Check that all variables are properly reinitialized

## Mock Response System

### Response Types

The debug tool generates three types of mock responses based on the question:

#### 1. Improvements Focus Response
```markdown
# Improved Summary - Focus on Improvements

## 🎉 Positive Highlights
This is an improved version focusing on positive aspects.

**Improvement applied:** Emphasized positive trends and success stories.
```

#### 2. Risk Highlight Response
```markdown
# Improved Summary - Risk Focus

## ⚠️ Risk Areas
This is an improved version focusing on risks and concerns.

**Improvement applied:** Highlighted security risks and areas needing attention.
```

#### 3. Enhanced Metrics Response
```markdown
# Improved Summary - Enhanced Metrics

## 📊 Detailed Analysis
This is an improved version with more detailed metrics.

**Improvement applied:** Added more statistical analysis and metrics.
```

### Context Simulation

Each mock response includes:
- **Original Context**: Shows what context was provided to the mock Amazon Q
- **Applied Improvement**: Describes what type of improvement was applied
- **Formatted Response**: Professional markdown formatting similar to real Amazon Q responses

## Debugging Scenarios

### Common Issues to Test

#### 1. Session State Loss
- **Scenario**: User clicks quick action button and loses AI summary
- **Test**: Verify that original summary persists in session state
- **Expected**: Original summary should remain accessible throughout

#### 2. Chat History Corruption
- **Scenario**: Chat history gets corrupted or lost during interactions
- **Test**: Perform multiple chat interactions and verify history integrity
- **Expected**: All conversations should be stored and retrievable

#### 3. Pending Question Handling
- **Scenario**: Pending questions not processed correctly
- **Test**: Click quick action buttons and verify processing flow
- **Expected**: Questions should be processed once and cleared immediately

#### 4. Summary Replacement Issues
- **Scenario**: Improved summary not stored or displayed correctly
- **Test**: Generate improved summary and verify storage/display
- **Expected**: Improved summary should be stored and displayed while preserving original

### Validation Checklist

- [ ] Original AI summary initializes correctly
- [ ] Quick action buttons set pending questions
- [ ] Pending questions are processed exactly once
- [ ] Mock responses are generated appropriately
- [ ] Chat history accumulates correctly
- [ ] Summary replacement works properly
- [ ] Context generation includes current summary
- [ ] State reset clears all variables
- [ ] Application recovers gracefully from state loss

## Integration with Main Application

### Session State Variables

The debug tool uses the same session state variables as the main application:

```python
st.session_state.original_ai_summary      # Original AI-generated summary
st.session_state.improved_summary         # User-improved summary version
st.session_state.chat_history            # List of (question, response) tuples
st.session_state.pending_quick_question   # Currently pending quick question
st.session_state.ai_summary_generated     # Flag indicating summary generation
```

### Workflow Simulation

The debug tool simulates the exact workflow used in the main application:
1. **Button Click** → Set pending question in session state
2. **State Rerun** → Streamlit reruns the application
3. **Question Processing** → Pending question is processed and cleared
4. **Response Handling** → Response is added to chat history
5. **Summary Update** → Optional summary replacement

## Best Practices

### When to Use the Debug Tool

- **Before Deploying Changes**: Validate session state behavior after code modifications
- **Troubleshooting Issues**: Investigate reported session state problems
- **Testing New Features**: Verify that new chat features work correctly
- **Performance Testing**: Check behavior under various interaction patterns

### Testing Recommendations

1. **Start Fresh**: Always begin testing with a clean session state
2. **Test Systematically**: Follow the testing workflow step by step
3. **Verify Persistence**: Ensure state persists across multiple interactions
4. **Test Edge Cases**: Try rapid button clicking and unusual interaction patterns
5. **Validate Recovery**: Test application behavior after state corruption

## Troubleshooting

### Common Debug Tool Issues

#### Tool Won't Start
- **Check Dependencies**: Ensure Streamlit is installed
- **Verify Path**: Run from the correct directory
- **Check Permissions**: Ensure script has execute permissions

#### Mock Responses Not Generated
- **Check Logic**: Verify question type detection logic
- **Review Context**: Ensure context generation is working
- **Check State**: Verify session state variables are set correctly

#### State Not Persisting
- **Browser Issues**: Try refreshing the browser or clearing cache
- **Streamlit Issues**: Restart the Streamlit server
- **Code Issues**: Check for session state key conflicts

## Contributing

When modifying the debug tool:

1. **Maintain Compatibility**: Ensure session state variables match the main application
2. **Update Documentation**: Keep this documentation current with changes
3. **Test Thoroughly**: Validate that debug functionality works correctly
4. **Preserve Mock Logic**: Maintain realistic mock response generation

## Related Documentation

- [Session State Fix Documentation](session-state-fix.md) - Detailed explanation of session state issues and solutions
- [Amazon Q Integration](amazon-q-integration.md) - Information about Amazon Q CLI integration
- [Main README](../README.md) - Complete application documentation

This debug tool is essential for maintaining the reliability and user experience of the CHI Analyzer's AI chat functionality.