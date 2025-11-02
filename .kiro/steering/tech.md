# Technology Stack

## Core Technologies

- **Python 3.12.3**: Primary programming language
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis library
- **OpenPyXL**: Excel file reading and writing
- **Plotly**: Interactive data visualization and charting
- **ReportLab**: PDF report generation (optional dependency)
- **Amazon Q CLI**: AI-powered summary generation

## Key Dependencies

```python
# Core data processing
pandas
openpyxl

# Web application
streamlit

# Visualization
plotly

# PDF generation (optional)
reportlab

# Additional utilities
logging (built-in)
subprocess (built-in)
datetime (built-in)
re (built-in)
```

## Development Environment

- **Virtual Environment**: `chi_analyzer_env/` (Python venv)
- **Platform**: Cross-platform (developed on Ubuntu, Windows compatible)

## Common Commands

### Setup and Installation
```bash
# Create virtual environment
python3 -m venv chi_analyzer_env

# Activate environment (Linux/Mac)
source chi_analyzer_env/bin/activate

# Activate environment (Windows)
chi_analyzer_env\Scripts\activate

# Install dependencies
pip install streamlit pandas openpyxl plotly

# Install optional PDF export dependency
pip install reportlab
```

### Running the Application
```bash
# Start Streamlit app
streamlit run chi_low_security_score_analyzer.py

# Run with specific port
streamlit run chi_low_security_score_analyzer.py --server.port 8501
```

### Amazon Q CLI Setup
```bash
# Install Amazon Q CLI (if not already installed)
# Follow AWS documentation for installation

# Login to Amazon Q
q auth login

# Test connection
q chat "hello"
```

## File Processing Notes

- **Excel Format**: Expects .xlsx files with specific column naming conventions
- **Header Detection**: Automatically scans rows 0-20 to find header row
- **Column Matching**: Uses case-insensitive regex matching for "Security Score", "Customer", "Overall Score"
- **Date Sheet Format**: Expects sheet names in "YYYY-MM-DD" format for historical analysis

## Enhanced PDF Export Notes

- **Optional Dependency**: PDF export requires `reportlab` library
- **Layout**: Multi-page A4 portrait format with professional design
- **Content**: Comprehensive reports including:
  - Executive summary with color-coded metrics
  - Detailed customer analysis with scores and changes
  - AI insights in highlighted sections
  - Professional typography and visual elements
- **Scalability**: Handles large datasets with automatic truncation and pagination
- **Graceful Degradation**: Application works without reportlab, PDF export simply unavailable