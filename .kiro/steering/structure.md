# Project Structure

## Root Directory Layout

```
chi-monthly-report/
├── chi_low_security_score_analyzer.py    # Main Streamlit application
├── chi-monthly-summary.md                # Sample output summary
├── amazon_q_cli.log                      # Amazon Q CLI operation logs
├── chi_analyzer_env/                     # Python virtual environment
├── .kiro/                               # Kiro IDE configuration
│   └── steering/                        # AI assistant guidance files
└── ai_summary_*.md                      # Generated AI summaries (timestamped)
```

## File Organization Patterns

### Core Application
- **Single-file architecture**: All functionality contained in `chi_low_security_score_analyzer.py`
- **Monolithic design**: UI, data processing, and AI integration in one module

### Generated Files
- **AI Summaries**: Auto-generated with timestamp format `ai_summary_YYYYMMDD_HHMMSS.md`
- **Log Files**: `amazon_q_cli.log` for debugging Amazon Q CLI interactions
- **Output Reports**: Excel files generated in-memory and downloaded by users

### Virtual Environment
- **Location**: `chi_analyzer_env/` directory
- **Type**: Python venv (not conda or pipenv)
- **Activation**: Platform-specific scripts in `bin/` (Linux/Mac) or `Scripts/` (Windows)

## Code Organization Within Main File

### Function Categories
1. **Logging Setup**: `setup_logging()`, logger initialization
2. **Amazon Q Integration**: `generate_ai_summary()`, `check_amazon_q_availability()`, `clean_ansi_codes()`
3. **Data Processing**: `_first_nonempty_row_as_header()`, `_coerce_numeric()`, `_normalize_colnames()`
4. **Analysis Logic**: `classify()`, `calculate_low_score_metrics()`, `calculate_monthly_changes()`
5. **Visualization**: `create_trend_chart()`, `extract_historical_data()`
6. **Export Functions**: `export_excel()`, `export_pdf()`, `summarize_tables()`
7. **Streamlit UI**: Main application flow and user interface

### Naming Conventions
- **Private functions**: Prefix with underscore (`_first_nonempty_row_as_header`)
- **Public functions**: Descriptive names (`calculate_low_score_metrics`)
- **Constants**: Uppercase for thresholds and configuration
- **Variables**: Snake_case for all variables and function names

## Data Flow Architecture

1. **Input**: Excel file upload via Streamlit
2. **Processing**: Pandas-based data manipulation and classification
3. **Analysis**: Statistical calculations and trend analysis
4. **AI Enhancement**: Amazon Q CLI integration for summary generation
5. **Visualization**: Plotly charts and Streamlit components
6. **Output**: Excel export and markdown summaries

## Configuration Management

- **No external config files**: All settings managed through Streamlit UI
- **Environment variables**: None currently used
- **Hardcoded values**: Threshold defaults, column name patterns, file paths