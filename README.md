# CHI Low Security Score Analyzer

A Streamlit-based web application for analyzing Customer Health Index (CHI) security score data. This tool helps Technical Account Managers (TAMs) track customer security posture changes month-over-month and identify customers requiring attention.

**Current Version: 2.0.7** - Enhanced PDF export with Amazon Q chat history integration, comprehensive conversation documentation in reports

## Features

### Core Analysis
- **Excel Data Processing**: Upload monthly CHI Excel files containing customer security scores
- **Flexible Comparison Modes**: 
  - Compare two columns within Sheet1 (e.g., October vs September scores)
  - Compare two dated sheets (e.g., "2025-09-08" vs "2025-10-06")
- **Customer Classification**: Automatically categorizes customers into four groups:
  - Exit from Red (improved security scores)
  - Return Back to Red (deteriorated scores)
  - New Comer to Red (new customers with low scores)
  - Missing from CHI (customers without data)

### Advanced Analytics
- **Historical Trend Analysis**: 
  - Multi-month security score tracking across all dated sheets
  - Interactive trend charts with Plotly visualizations and enhanced controls
  - Chart interaction features: zoom, pan, select, and download capabilities
  - Month-over-month improvement metrics and percentages
  - Automatic detection of historical data patterns
- **Risk Assessment Dashboard**: 
  - Color-coded risk levels (High/Medium/Low)
  - Improvement ratio calculations
  - Real-time security posture evaluation

### AI-Powered Features
- **Amazon Q CLI Integration**: 
  - Optimized multi-layered authentication detection for improved reliability
  - Seamless login/logout management within the application
  - Automatic status detection with enhanced performance and error resilience
  - Enhanced error handling and troubleshooting guidance
- **Intelligent Summary Generation**: 
  - AI-powered monthly reports with professional formatting
  - Context-aware analysis based on actual customer data
  - Automatic file saving with timestamps
  - Enhanced debug logging for troubleshooting generation issues
- **Interactive Chat Interface**: 
  - Real-time conversation with Amazon Q about your data
  - Context-aware responses based on uploaded CHI information
  - Multi-turn conversations with chat history
  - Predefined quick questions for common analysis needs
  - Summary improvement and customization through chat
  - Enhanced session state management for seamless interactions
  - Persistent AI summary storage to prevent data loss during chat
  - Intelligent AI summary caching for improved performance and user experience
  - Comprehensive debug logging for AI summary generation and caching behavior
  - Enhanced debug output with explicit flushing for immediate visibility of button interactions
  - Real-time debug message display with sys.stdout.flush() for better troubleshooting

### Export & Reporting
- **Enhanced Excel Reports**: Comprehensive multi-sheet workbooks with summary statistics and detailed customer lists per category
- **Professional PDF Reports**: 
  - Multi-page A4 format with rich visual design
  - Executive summary with color-coded metrics dashboard
  - Detailed customer analysis with scores and changes
  - AI-generated insights in highlighted sections
  - **Chat History Integration**: Complete Amazon Q conversation history included in PDF reports
  - Interactive chat questions and AI responses preserved in professional format
  - Professional typography with emoji icons and visual elements
  - Scalable content handling for large datasets
  - Graceful degradation when reportlab is unavailable

## Installation

### Prerequisites

- Python 3.12.3 or higher
- Amazon Q CLI (optional, for AI summaries)

### Quick Installation

**Option A - WSL Deployment (Recommended for Windows):**

1. **Install and setup:**
   ```bash
   chmod +x install.sh wsl-config.sh deploy-wsl.sh
   ./install.sh
   ./wsl-config.sh
   ```

2. **Deploy in WSL:**
   ```bash
   ./deploy-wsl.sh
   ```
   
   Or from Windows: Double-click `start-wsl.bat`

**Option B - Standard Installation:**

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Manual Setup

1. **Clone or download the project files**

2. **Create a virtual environment**:
   ```bash
   python3 -m venv chi_analyzer_env
   ```

3. **Activate the virtual environment**:
   
   **Linux/Mac:**
   ```bash
   source chi_analyzer_env/bin/activate
   ```
   
   **Windows:**
   ```bash
   chi_analyzer_env\Scripts\activate
   ```

4. **Install dependencies**:
   
   **Option A - Using requirements.txt (recommended):**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Option B - Manual installation:**
   ```bash
   pip install streamlit pandas openpyxl plotly reportlab
   ```
   
   **Option C - Core dependencies only:**
   ```bash
   pip install streamlit pandas openpyxl plotly
   ```
   
   **Option D - Development environment:**
   ```bash
   pip install -r requirements-dev.txt
   ```
   
   **Note**: The application works without reportlab, but enhanced PDF export will be unavailable.

### Amazon Q CLI Setup (Optional)

For AI-powered summary generation and interactive chat:

**📖 Complete Installation Guides:**
- **[WSL/Linux Installation Guide](docs/amazon-q-cli-installation.md)** - Comprehensive guide for WSL and Linux environments with detailed troubleshooting
- **[Windows & WSL Installation Guide](docs/amazon-q-cli-windows-wsl.md)** - Detailed guide for Windows and WSL environments based on AWS official blog

The comprehensive installation guides cover:
- **Multiple Installation Methods**: Official script, manual download, user directory installation, GitHub releases
- **WSL-Specific Instructions**: Detailed setup for Windows Subsystem for Linux with path configuration
- **Windows Environment**: PowerShell, Chocolatey, and Scoop installation methods
- **Network Troubleshooting**: Solutions for proxy environments, DNS issues, and enterprise firewalls
- **Authentication Management**: Login/logout procedures, status verification, and credential management
- **Integration with CHI Analyzer**: Application-specific configuration, testing, and troubleshooting
- **Security Best Practices**: Authentication security, network considerations, and permission management

#### Quick Installation Options:

1. **GitHub Download (Recommended)**:
   ```bash
   curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
   chmod +x q && sudo mv q /usr/local/bin/
   q login
   ```

2. **User Directory Installation (No sudo required)**:
   ```bash
   mkdir -p ~/.local/bin
   curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
   chmod +x ~/.local/bin/q
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
   q login
   ```

3. **User Directory Installation (No sudo required)**:
   ```bash
   mkdir -p ~/.local/bin
   wget -O ~/.local/bin/q https://d2yblsmsllhwuq.cloudfront.net/q/releases/latest/q-linux-amd64
   chmod +x ~/.local/bin/q
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   q login
   ```

#### Application Integration:
- **Built-in Login Management**: Use the sidebar login/logout buttons
- **Automatic Status Detection**: Real-time authentication status display
- **Integrated Troubleshooting**: In-app guidance for common issues

### Enhanced AI Features

Once Amazon Q CLI is configured, you can:
- **Generate AI Summaries**: Professional monthly reports with intelligent analysis
- **Interactive Chat**: Real-time conversation about your data with context awareness
- **Summary Improvement**: Use chat to refine and customize generated summaries
- **Quick Analysis**: Predefined questions for common TAM scenarios
- **Multi-turn Conversations**: Maintain context across multiple questions

## Usage

### WSL Deployment (Recommended)

1. **Start the application**:
   ```bash
   ./deploy-wsl.sh
   ```
   
   Or use the alias:
   ```bash
   chi-analyzer
   ```
   
   Or from Windows: Double-click `start-wsl.bat`

### Standard Deployment

1. **Start the application**:
   ```bash
   streamlit run chi_low_security_score_analyzer.py
   ```

2. **Open your browser** to the displayed URL (typically `http://localhost:8501`)

3. **Upload your CHI Excel file** containing customer security score data

4. **Configure analysis settings**:
   - Set security score threshold (default: 42)
   - Choose comparison mode (columns or sheets)
   - Select the appropriate columns or sheets to compare

5. **Review results**:
   - View comprehensive analysis dashboard with risk assessment
   - Examine interactive trend charts with full zoom, pan, and export controls
   - Use scroll zoom and selection tools for detailed data exploration
   - Review detailed metrics including improvement percentages
   - Analyze month-over-month changes and patterns

6. **AI-Enhanced Analysis** (if Amazon Q CLI is configured):
   - Generate intelligent monthly summaries with professional formatting (cached for performance)
   - Use interactive chat to ask specific questions about your data
   - Improve and customize summaries through conversational AI
   - Get context-aware insights and recommendations
   - Benefit from intelligent caching that eliminates regeneration delays

7. **Export comprehensive reports**:
   - Download multi-sheet Excel reports with detailed customer breakdowns
   - Generate professional PDF reports with executive summaries and visual elements
   - Save AI-generated summaries as markdown files

## File Format Requirements

### Excel File Structure

- **File Format**: `.xlsx` files
- **Header Detection**: Application automatically scans rows 0-20 to find headers
- **Required Columns**: Must contain columns matching these patterns (case-insensitive):
  - Customer names: "Customer"
  - Security scores: "Security Score"
  - Overall scores: "Overall Score"

### Sheet Naming for Historical Analysis

- **Date Format**: Sheet names should follow "YYYY-MM-DD" format
- **Example**: "2025-09-08", "2025-10-06"

## Export Formats

### Excel Reports
- Multi-sheet workbook with summary statistics
- Separate sheets for each customer category
- Detailed customer information and score changes

### Enhanced PDF Reports
- **Professional Layout**: Multi-page A4 portrait format with rich visual design
- **Executive Summary**: Comprehensive metrics dashboard with color-coded statistics and percentages
- **Detailed Analysis**: Category-wise customer breakdowns with scores and changes
- **AI Insights**: Highlighted AI-generated summaries and recommendations (when available)
- **Chat History Documentation**: Complete Amazon Q conversation history with questions and responses
- **Interactive Analysis Record**: Preserves all chat interactions for comprehensive reporting
- **Visual Elements**: Emoji icons, color-coded sections, and professional typography
- **Complete Data**: Customer names, current/previous scores, score changes, and trend analysis
- **Scalable Content**: Handles large customer lists with automatic pagination and "and X more..." indicators
- **Graceful Degradation**: Application works seamlessly without reportlab, with clear user guidance

## Target Users

- Technical Account Managers (TAMs)
- Customer Success Teams
- Security Operations Teams
- Anyone tracking customer security health metrics

## Troubleshooting

### PDF Export Issues
If PDF export is not available:
- Install reportlab: `pip install reportlab`
- The application will work without PDF export if reportlab is not installed

### Amazon Q CLI Issues
- **Installation & Setup**: See comprehensive installation guides:
  - [WSL/Linux Installation Guide](docs/amazon-q-cli-installation.md) for detailed WSL and Linux setup
  - [Windows & WSL Installation Guide](docs/amazon-q-cli-windows-wsl.md) for Windows-specific instructions
- **Enhanced Authentication Detection**: New multi-layered status checking provides better reliability:
  - Fast login status verification (5s timeout)
  - Help command accessibility test (3s timeout)
  - Simple chat functionality test (8s timeout)
  - Graceful handling of network delays and partial failures
- **Authentication**: Use the built-in login button or manually run `q login`
- **Status Check**: The application provides real-time status updates with improved accuracy
- **Credentials**: Check your AWS credentials and Amazon Q permissions
- **Logs**: Review the `amazon_q_cli.log` file for detailed error messages and debugging information
- **Debug Output**: Check console output for detailed AI summary generation and caching debug information with enhanced flushing for immediate visibility
- **Real-time Debugging**: Enhanced debug messages with explicit flushing provide immediate feedback for button interactions and session state changes
- **Chat Issues**: If chat fails, check authentication status and try refreshing
- **Timeout Problems**: New staged timeout approach handles network issues better
- **WSL-Specific Issues**: Refer to the installation guides for comprehensive WSL troubleshooting

### Session State and Chat Issues
- **Session State Problems**: Use the debug tool to investigate state persistence issues:
  ```bash
  streamlit run debug-session-state.py
  ```
- **Chat History Loss**: The debug tool can help validate chat history management
- **Summary Disappearing**: Test summary persistence with the interactive debug interface
- **Button Interaction Issues**: Use mock responses to test without Amazon Q CLI dependency
- **State Reset**: The debug tool provides complete session state reset functionality

### Excel File Issues
- Ensure your file is in `.xlsx` format
- Verify column names match expected patterns
- Check that data starts within the first 20 rows

## Development

### Technology Stack

The application is built with:
- **Python 3.12.3**: Core programming language
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis library
- **Plotly**: Interactive data visualization and charting
- **OpenPyXL**: Excel file reading and writing
- **ReportLab**: PDF report generation (optional dependency)
- **Amazon Q CLI**: AI-powered summary generation and chat interface

### Development Environment

- **Virtual Environment**: `chi_analyzer_env/` (Python venv)
- **Platform**: Cross-platform (developed on Ubuntu, Windows compatible)
- **Dependencies**: See `requirements.txt` for complete list

### Testing and Quality Assurance

**📖 Complete Testing Guide**: See [Testing Framework Documentation](docs/testing-framework.md) for comprehensive testing procedures and best practices.

#### Session State Testing
The application includes dedicated test scripts for verifying session state persistence:

**`test-session-state-fix.py`** - Interactive test utility for session state management:
- **Purpose**: Validates that session state persists correctly across button interactions
- **Features**: 
  - Tests AI summary persistence during chat interactions
  - Verifies chat history maintenance
  - Validates quick question button functionality
  - Simulates real-world user interaction patterns
- **Usage**: Run with `streamlit run test-session-state-fix.py`
- **Test Coverage**:
  - Session state initialization and persistence
  - Button click handling without data loss
  - Chat history management
  - Pending question state handling
  - State reset functionality

**`debug-session-state.py`** - Advanced debugging tool for session state behavior:
- **Purpose**: Interactive debugging interface for session state management
- **Features**:
  - Real-time session state inspection and monitoring
  - Mock Amazon Q responses for testing without CLI dependency
  - Interactive quick action buttons with immediate feedback
  - Chat history visualization and management
  - Context generation testing and validation
  - Complete session state reset functionality
- **Usage**: Run with `streamlit run debug-session-state.py`
- **Debug Capabilities**:
  - View current session state variables and their values
  - Test pending question handling with mock responses
  - Simulate different improvement scenarios (focus on improvements, highlight risks, add metrics)
  - Validate context generation for Amazon Q integration
  - Test summary replacement and improvement workflows
  - Monitor chat history accumulation and management

**`simulate-user-interaction.py`** - User interaction simulation and debug flow testing:
- **Purpose**: Simulates complete user interaction workflows to test debug flow and AI summary behavior
- **Features**:
  - Comprehensive simulation of CHI analysis workflow with realistic data
  - AI summary generation and caching behavior testing
  - Session state management validation across user interactions
  - Context generation testing for Amazon Q CLI integration
  - Debug output visualization for troubleshooting
  - Mock Streamlit session state for standalone testing
- **Usage**: Run with `python simulate-user-interaction.py`
- **Test Scenarios**:
  - AI summary generation with caching behavior analysis
  - Quick question button simulation and processing
  - Context generation for Amazon Q CLI prompts
  - Session state persistence across interactions
  - Debug logging output validation
- **Debug Output**: Shows exactly what context and prompts would be sent to Amazon Q CLI

#### Running Tests
```bash
# Test complete workflow with Amazon Q integration
python test-full-workflow.py

# Validate PDF chat history feature (no dependencies)
python validate-pdf-chat-feature.py

# Test PDF export with chat history integration (requires reportlab)
python test-pdf-with-chat.py

# Test session state handling
streamlit run test-session-state-fix.py

# Debug session state behavior (advanced)
streamlit run debug-session-state.py

# Simulate user interactions and debug flow
python simulate-user-interaction.py

# Test Amazon Q CLI status and authentication
python test-amazon-q-status.py

# Test simple chat functionality
python test-simple-chat.py

# Test main application
streamlit run chi_low_security_score_analyzer.py
```

#### Full Workflow Testing

**`test-full-workflow.py`** - Comprehensive end-to-end workflow validation:
- **Purpose**: Tests the complete CHI analyzer workflow including Amazon Q integration
- **Features**:
  - Simulates realistic CHI analysis data with customer metrics
  - Tests Amazon Q context generation and response quality
  - Validates context preservation across multiple interactions
  - Tests summary improvement workflows with realistic scenarios
  - Verifies that Amazon Q responses are relevant and contextual
- **Usage**: Run with `python test-full-workflow.py`
- **Test Scenarios**:
  - Basic Amazon Q chat with CHI analysis context
  - Context preservation when building on previous summaries
  - Summary improvement requests (focus on positives, add metrics)
  - Response relevance validation
  - Timeout and error handling

#### Development Best Practices
- **Full Workflow Testing**: Use `test-full-workflow.py` to validate end-to-end functionality before releases
- **Session State Management**: Use the test script to verify state persistence before deploying changes
- **Interactive Testing**: Test all button interactions to ensure no data loss occurs
- **State Isolation**: Ensure different session state keys don't interfere with each other
- **Error Recovery**: Test application behavior when session state is corrupted or missing
- **Amazon Q Integration**: Validate context generation and response quality with realistic data

## Technical Documentation

### Comprehensive Documentation Suite

The project includes extensive technical documentation covering all aspects of the system:

**📖 Core Documentation:**
- **[Installation Guides](docs/amazon-q-cli-installation.md)** - Complete setup instructions for all platforms
- **[Testing Framework](docs/testing-framework.md)** - Comprehensive testing procedures and best practices
- **[Enhanced Features](docs/enhanced-features.md)** - Detailed feature documentation and usage guides

**📖 Advanced Technical Guides:**
- **[GenAI Report & Amazon Q CLI Session Management](docs/genai-report-and-qcli-session-management.md)** - Comprehensive technical documentation covering:
  - State management architecture and session persistence
  - AI summary generation and caching mechanisms
  - Amazon Q CLI session handling and multi-turn conversations
  - Button interaction processing and UI state management
  - Error handling, recovery strategies, and performance optimization
  - Debug monitoring and troubleshooting procedures
- **[Session State Management](docs/session-state-fix.md)** - Session state persistence and debugging
- **[Amazon Q Integration](docs/amazon-q-integration.md)** - AI integration architecture and implementation

**📖 Specialized Guides:**
- **[Enhanced PDF with Chat](docs/enhanced-pdf-with-chat.md)** - PDF export with chat history integration
- **[Authentication Improvements](docs/authentication-improvements-v2.0.3.md)** - Multi-layered authentication system
- **[Performance Optimization](docs/amazon-q-performance-optimization.md)** - Performance tuning and optimization strategies
- **[Cache Duration Analysis](docs/cache-duration-analysis.md)** - Detailed analysis of Amazon Q CLI caching mechanisms (5-minute vs 10-minute cache comparison)

## Documentation Status

All documentation has been reviewed and updated as of version 2.0.7 (2025-11-03):

- ✅ **Installation Guides**: Comprehensive and current
- ✅ **Feature Documentation**: Complete with PDF chat history integration details
- ✅ **Testing Framework**: Updated with new PDF export validation tests
- ✅ **Technical Architecture**: Comprehensive GenAI and session management documentation
- ✅ **API References**: Up-to-date with chat history parameter documentation
- ✅ **Troubleshooting**: Detailed solutions provided with debug output guidance
- ✅ **Cross-References**: Validated and consistent

## License

This project is for internal use. Please follow your organization's guidelines for code sharing and distribution.