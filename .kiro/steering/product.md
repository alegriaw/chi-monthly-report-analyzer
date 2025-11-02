# Product Overview

## CHI Low Security Score Analyzer

A Streamlit-based web application for analyzing Customer Health Index (CHI) security score data. The tool helps Technical Account Managers (TAMs) track customer security posture changes month-over-month and identify customers requiring attention.

### Core Functionality

- **Excel Data Processing**: Upload monthly CHI Excel files containing customer security scores
- **Comparison Modes**: 
  - Compare two columns within Sheet1 (e.g., October vs September scores)
  - Compare two dated sheets (e.g., "2025-09-08" vs "2025-10-06")
- **Customer Classification**: Automatically categorizes customers into four groups:
  - Exit from Red (improved security scores)
  - Return Back to Red (deteriorated scores)
  - New Comer to Red (new customers with low scores)
  - Missing from CHI (customers without data)
- **AI-Powered Summaries**: Integrates with Amazon Q CLI to generate professional monthly reports
- **Trend Analysis**: Historical tracking and visualization of security score patterns
- **Export Capabilities**: Generate Excel and PDF reports with summary and detailed customer lists

### Target Users

Technical Account Managers (TAMs) and customer success teams who need to monitor and report on customer security health metrics.

### Export Formats

- **Excel Reports**: Comprehensive multi-sheet workbooks with summary statistics and detailed customer lists per category
- **Enhanced PDF Reports**: Professional multi-page reports with rich formatting and complete analysis, including:
  - Executive summary with color-coded metrics dashboard
  - Detailed customer analysis with scores and changes
  - AI-generated insights in highlighted sections
  - Professional layout with emoji icons and visual elements
  - Scalable content handling for large datasets
  - Multi-page support with consistent formatting

### Key Value Proposition

Transforms raw CHI security data into actionable insights, enabling proactive customer engagement and systematic security posture improvement tracking.