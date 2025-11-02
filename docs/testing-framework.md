# CHI Analyzer Testing Framework

## Overview

The CHI Low Security Score Analyzer includes a comprehensive testing framework to ensure reliability and quality across all features, particularly the complex Amazon Q integration and session state management.

## Test Suite Components

### 1. Full Workflow Testing (`test-full-workflow.py`)

**Purpose**: End-to-end validation of the complete CHI analyzer workflow

**Key Features**:
- Simulates realistic CHI analysis data with customer security metrics
- Tests Amazon Q CLI integration with proper context generation
- Validates context preservation across multiple chat interactions
- Tests summary improvement workflows with realistic user scenarios
- Verifies response relevance and quality
- Enhanced debug output validation with explicit flushing for improved testing visibility
- Real-time debug message display with sys.stdout.flush() for immediate feedback during testing

**Test Scenarios**:

#### Basic Amazon Q Integration Test
```python
# Simulates CHI analysis data
analysis_data = {
    'exit_from_red': 5,
    'return_back_red': 3,
    'new_comer_red': 2,
    'missing_from_chi': 1,
    'total_customers': 11,
    'low_score_improvement_pct': 18.2
}
```

- Creates realistic context with customer metrics
- Tests "Focus on improvements" question type
- Validates Amazon Q response relevance
- Checks for appropriate keywords in responses

#### Context Preservation Test
- Tests that improved summaries are properly used as context
- Validates that Amazon Q builds on previous responses
- Ensures context continuity across multiple interactions
- Verifies that summary improvements persist

**Usage**:
```bash
python test-full-workflow.py
```

**Expected Output**:
- Test results for basic Amazon Q chat functionality
- Context preservation validation results
- Response relevance assessment
- Overall workflow status (PASS/FAIL)

### 2. Session State Testing (`test-session-state-fix.py`)

**Purpose**: Interactive validation of session state persistence

**Features**:
- Tests AI summary persistence during chat interactions
- Verifies chat history maintenance
- Validates quick question button functionality
- Simulates real-world user interaction patterns

**Usage**:
```bash
streamlit run test-session-state-fix.py
```

### 3. Debug Session State (`debug-session-state.py`)

**Purpose**: Advanced debugging interface for session state behavior

**Features**:
- Real-time session state inspection
- Mock Amazon Q responses for testing without CLI dependency
- Interactive quick action buttons with immediate feedback
- Complete session state reset functionality

**Usage**:
```bash
streamlit run debug-session-state.py
```

### 4. Amazon Q Status Testing (`test-amazon-q-status.py`)

**Purpose**: Validates Amazon Q CLI authentication and availability

**Features**:
- Tests Amazon Q CLI installation and authentication
- Validates login status detection
- Tests basic chat functionality
- Provides troubleshooting guidance

**Usage**:
```bash
python test-amazon-q-status.py
```

### 5. Simple Chat Testing (`test-simple-chat.py`)

**Purpose**: Basic Amazon Q chat functionality validation

**Features**:
- Tests simple chat interactions
- Validates response format and content
- Checks error handling for failed requests

**Usage**:
```bash
python test-simple-chat.py
```

### 6. PDF Export with Chat History Testing (`test-pdf-with-chat.py`)

**Purpose**: Validates PDF export functionality with Amazon Q chat history integration

**Features**:
- Tests PDF generation with complete chat conversation history
- Validates chat history formatting and presentation in PDF reports
- Tests multi-conversation scenarios with questions and responses
- Verifies professional PDF layout with chat integration
- Ensures graceful handling of large chat histories

**Test Scenarios**:

#### Chat History Integration Test
```python
# Sample chat history with realistic TAM scenarios
chat_history = [
    (
        "Please rewrite the summary to focus more on the positive improvements and success stories.",
        "# CHI Security Analysis Summary - Success Focus\n\n## 🎉 Outstanding Achievements..."
    ),
    (
        "Add more specific metrics and percentages to this summary.",
        "# CHI Security Analysis Summary - Enhanced Metrics\n\n## 📊 Key Performance Indicators..."
    )
]
```

- Tests PDF generation with complete chat conversation history
- Validates professional formatting of questions and AI responses
- Ensures proper integration with existing PDF report structure
- Tests scalability with multiple conversation turns

**Usage**:
```bash
python test-pdf-with-chat.py
```

**Prerequisites**:
- ReportLab library: `pip install reportlab` (for actual PDF generation)
- Without ReportLab: Tests error handling and function signature validation

**Expected Output**:
- Function import validation
- ReportLab availability check
- PDF generation success confirmation (if ReportLab available)
- File size validation and test PDF creation
- Graceful error handling validation (if ReportLab unavailable)
- Comprehensive feature validation checklist

### 7. User Interaction Simulation (`simulate-user-interaction.py`)

**Purpose**: Comprehensive simulation of user interaction workflows to test debug flow and AI summary behavior

**Features**:
- Simulates complete CHI analysis workflow with realistic customer data
- Tests AI summary generation and caching behavior with detailed debug output
- Validates session state management across user interactions
- Tests context generation for Amazon Q CLI integration
- Provides comprehensive debug logging for troubleshooting
- Uses mock Streamlit session state for standalone testing

**Test Scenarios**:

#### AI Summary Generation and Caching Test
```python
# Simulates realistic CHI analysis data
analysis_data = {
    'exit_from_red': 5,
    'return_back_red': 3,
    'new_comer_red': 2,
    'missing_from_chi': 1,
    'total_customers': 11,
    'low_score_improvement_pct': 18.2
}
```

- Tests AI summary generation with caching behavior
- Validates session state persistence for AI summaries
- Shows debug output for generation vs. cached usage
- Tests summary length and content preview logging

#### Quick Question Button Simulation
- Simulates "Focus on improvements" button click
- Tests pending question state management
- Validates context generation for Amazon Q prompts
- Shows complete prompt that would be sent to Amazon Q CLI

#### Debug Output Validation
- Comprehensive debug logging throughout the simulation
- Shows session state changes and persistence behavior
- Displays context generation process step-by-step
- Provides visibility into AI summary caching decisions

**Usage**:
```bash
python simulate-user-interaction.py
```

**Expected Output**:
- Detailed debug logging with 🔍 DEBUG: prefixes
- AI summary generation and caching behavior analysis
- Complete Amazon Q CLI prompt preview
- Session state management validation results
- Context generation process visualization

## Testing Best Practices

### Pre-Release Testing Checklist

1. **Full Workflow Validation**:
   ```bash
   python test-full-workflow.py
   ```
   - Ensure all tests pass
   - Verify response relevance
   - Check context preservation

2. **Session State Verification**:
   ```bash
   streamlit run test-session-state-fix.py
   ```
   - Test all button interactions
   - Verify no data loss occurs
   - Validate chat history persistence

3. **PDF Export with Chat History**:
   ```bash
   # Validate function signature and parameters (no dependencies required)
   python validate-pdf-chat-feature.py
   
   # Full PDF generation test (requires reportlab)
   python test-pdf-with-chat.py
   ```
   - Validate function signature and chat history parameter support
   - Test PDF generation with chat conversation history
   - Verify professional formatting of chat interactions
   - Validate multi-conversation scenario handling
   - Check PDF file generation and size

4. **User Interaction Simulation**:
   ```bash
   python simulate-user-interaction.py
   ```
   - Test AI summary generation and caching behavior
   - Validate debug flow and logging output
   - Check context generation for Amazon Q integration
   - Verify session state management across interactions

5. **Amazon Q Integration**:
   ```bash
   python test-amazon-q-status.py
   ```
   - Confirm authentication status
   - Test basic chat functionality
   - Validate error handling

6. **Interactive Testing**:
   ```bash
   streamlit run debug-session-state.py
   ```
   - Test with mock responses
   - Verify state management
   - Check edge cases

### Development Workflow

1. **Feature Development**: Implement new features with corresponding tests
2. **Unit Testing**: Run specific test scripts for modified components
3. **Debug Flow Testing**: Use `simulate-user-interaction.py` to validate AI summary and session state behavior
4. **Integration Testing**: Use `test-full-workflow.py` to validate end-to-end functionality
5. **Interactive Testing**: Use Streamlit-based tests for UI validation
6. **Regression Testing**: Run full test suite before releases

### Test Data Management

The testing framework uses realistic but anonymized data:
- Customer counts and percentages based on real-world scenarios
- Security score thresholds matching production values
- Improvement metrics reflecting typical TAM reporting needs

### Error Handling Validation

All tests include comprehensive error handling validation:
- Network timeout scenarios
- Authentication failures
- Invalid response formats
- Missing dependencies
- Graceful degradation testing

## Continuous Integration

The testing framework supports automated testing workflows:
- All tests can be run non-interactively
- Exit codes indicate success/failure status
- Detailed logging for troubleshooting
- Mock response capabilities for CI environments

## Troubleshooting Test Issues

### Common Test Failures

1. **Amazon Q Authentication Issues**:
   - Run `q login` manually
   - Check AWS credentials
   - Verify network connectivity

2. **Timeout Errors**:
   - Check network stability
   - Increase timeout values if needed
   - Test with simpler queries first

3. **Context Preservation Failures**:
   - Verify session state management
   - Check for state key conflicts
   - Test with debug tools

4. **Response Relevance Issues**:
   - Review context generation logic
   - Validate input data format
   - Check Amazon Q model behavior

5. **AI Summary Generation Issues** (Enhanced in v2.0.6):
   - Check console output for debug logging messages with immediate visibility
   - Verify summary caching behavior with enhanced debug output and explicit flushing
   - Monitor summary length and content preview in logs with real-time feedback
   - Confirm generation vs. cached usage patterns with improved debug visibility
   - Look for "🔍 DEBUG:" messages to track AI summary lifecycle with flush=True parameters
   - Use `simulate-user-interaction.py` to test AI summary behavior in isolation
   - Enhanced button interaction debugging with sys.stdout.flush() for immediate feedback
   - Real-time session state monitoring with improved debug message display

### Test Environment Setup

For optimal testing results:
- Ensure stable network connection
- Have Amazon Q CLI properly configured
- Use realistic test data
- Run tests in isolated environment
- Clear session state between test runs
- Monitor console output for debug logging information with enhanced real-time visibility
- Check for AI summary generation and caching debug messages with explicit flushing
- Observe immediate debug feedback for button interactions and session state changes

## Future Enhancements

Planned testing framework improvements:
- Automated regression testing
- Performance benchmarking
- Load testing for large datasets
- Cross-platform compatibility testing
- Enhanced mock response capabilities