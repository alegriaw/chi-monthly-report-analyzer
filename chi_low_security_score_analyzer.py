# CHI Low Security Score Analyzer — Streamlit App
# ------------------------------------------------
# Features
# - Upload an Excel file containing your monthly CHI "low security score" lists
# - Choose comparison mode:
#     (A) Compare two columns on Sheet1 (e.g., "Security Score (Oct-06)" vs "Security Score (Sept-08)")
#     (B) Compare two dated sheets (e.g., "2025-09-08" vs "2025-10-06")
# - Threshold control (default 42)
# - Outputs: summary counts + customer lists for 4 categories
#     Exit from Red, Return Back to Red, New Comer to Red, Missing from CHI
# - Exports an Excel report with a Summary sheet and per-category sheets
#
# How to run:
#   1) pip install streamlit pandas openpyxl
#   2) streamlit run app.py
# ------------------------------------------------

import io
import re
import subprocess
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Version information
try:
    from version import __version__, get_version
    APP_VERSION = get_version()
except ImportError:
    APP_VERSION = "1.0.0"

# PDF generation imports
try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    PDF_AVAILABLE = True
    print("✅ DEBUG: reportlab imported successfully, PDF_AVAILABLE = True")
except ImportError as e:
    PDF_AVAILABLE = False
    print(f"❌ DEBUG: reportlab import failed: {e}, PDF_AVAILABLE = False")

# Setup logging for Amazon Q CLI operations
def setup_logging():
    """Setup logging for Amazon Q CLI operations"""
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(log_dir, 'amazon_q_cli.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console for debugging
        ]
    )
    return logging.getLogger('amazon_q_cli')

# Initialize logger
logger = setup_logging()

# Amazon Q status cache to avoid frequent checks
_amazon_q_cache = {
    'status': None,
    'message': None,
    'timestamp': 0,
    'cache_duration': 600  # 10 minutes cache
}

# -------------------------------
# Amazon Q CLI Integration
# -------------------------------

def clean_ansi_codes(text: str) -> str:
    """Remove ANSI color codes and formatting from text"""
    import re
    # Remove ANSI escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', text)
    
    # Remove additional formatting codes that might remain
    cleaned = re.sub(r'\[[\d;]+m', '', cleaned)
    cleaned = re.sub(r'\[\d+m', '', cleaned)
    
    # Clean up extra whitespace and newlines
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)  # Multiple newlines to double
    cleaned = cleaned.strip()
    
    return cleaned

def chat_with_amazon_q(message: str, context: str = "") -> tuple[bool, str]:
    """Interactive chat with Amazon Q CLI"""
    try:
        print(f"🔍 DEBUG: chat_with_amazon_q() called")
        print(f"🔍 DEBUG: Message: {message[:100]}...")
        print(f"🔍 DEBUG: Context length: {len(context)} chars")
        print(f"🔍 DEBUG: Context preview: {context[:300]}...")
        logger.info(f"Sending chat message to Amazon Q: {message[:100]}...")
        
        # Combine context and message
        full_prompt = f"{context}\n\nUser Question: {message}" if context else message
        print(f"🔍 DEBUG: Full prompt length: {len(full_prompt)} chars")
        print(f"🔍 DEBUG: Full prompt preview: {full_prompt[:500]}...")
        
        # Call Amazon Q CLI
        print(f"🔍 DEBUG: Calling Amazon Q CLI with subprocess.run()")
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=90)
        print(f"🔍 DEBUG: Amazon Q CLI returned with code: {result.returncode}")
        
        logger.info(f"Amazon Q CLI chat completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            raw_output = result.stdout.strip()
            print(f"🔍 DEBUG: Raw output length: {len(raw_output)} chars")
            print(f"🔍 DEBUG: Raw output preview: {raw_output[:300]}...")
            clean_output = clean_ansi_codes(raw_output)
            print(f"🔍 DEBUG: Clean output length: {len(clean_output)} chars")
            
            if clean_output:
                logger.info("Amazon Q chat response received successfully")
                print(f"🔍 DEBUG: Returning SUCCESS with clean output")
                return True, clean_output
            else:
                print(f"🔍 DEBUG: Empty response after cleaning")
                return False, "Amazon Q returned an empty response"
        else:
            error_msg = result.stderr.strip()
            print(f"🔍 DEBUG: Error message: {error_msg}")
            logger.error(f"Amazon Q CLI chat error: {error_msg}")
            
            if "not logged in" in error_msg.lower():
                print(f"🔍 DEBUG: Not logged in error detected")
                return False, "Authentication required. Please login to Amazon Q CLI."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                print(f"🔍 DEBUG: Quota/limit error detected")
                return False, "Amazon Q usage limit reached. Please try again later."
            else:
                print(f"🔍 DEBUG: Other error detected")
                return False, f"Amazon Q error: {clean_ansi_codes(error_msg)}"
                
    except subprocess.TimeoutExpired:
        logger.error("Amazon Q CLI chat request timed out")
        return False, "Request timed out. Please try again with a shorter message."
    except FileNotFoundError:
        logger.error("Amazon Q CLI not found")
        return False, "Amazon Q CLI not found. Please ensure it's installed and configured."
    except Exception as e:
        logger.error(f"Error in Amazon Q chat: {str(e)}")
        return False, f"Error in Amazon Q chat: {str(e)}"


def generate_ai_summary(analysis_data: Dict) -> tuple[bool, str]:
    """Generate AI-powered summary using Amazon Q CLI"""
    try:
        logger.info("Starting AI summary generation...")
        
        # Prepare the prompt with analysis data
        prompt = f"""
        Based on the following CHI (Customer Health Index) security score analysis data, please generate a comprehensive monthly summary report in markdown format:

        Analysis Results:
        - Exit from Red (Improved): {analysis_data['exit_from_red']} customers
        - Return Back to Red (Deteriorated): {analysis_data['return_back_red']} customers  
        - New Comer to Red (New risks): {analysis_data['new_comer_red']} customers
        - Missing from CHI: {analysis_data['missing_from_chi']} customers
        - Total customers analyzed: {analysis_data['total_customers']}
        
        Low Score Trend Analysis (customers with security score < 42):
        - Previous month total low-score customers: {analysis_data['prev_month_low_total']}
        - Current month total low-score customers: {analysis_data['curr_month_low_total']}
        - Net improvement: {analysis_data['low_score_improvement_count']} customers
        - Improvement percentage: {analysis_data['low_score_improvement_pct']:.1f}%

        Please write a professional summary including the following key points:
        1. Highlights the overall low-score trend and improvement metrics
        2. Analyzes the movement between categories (Exit, Return, New Comer)
        3. Congratulates customers who improved their security posture
        4. Identifies areas needing attention and specific customer segments
        5. Encourages TAM teams to maintain regular reviews and focus areas
        6. Provides an overall assessment of the security posture changes
        
        Format the summary response in clean markdown limited to 200 to 300 words in paragraph , emphasis, but no bullet points. Write in a professional, encouraging tone suitable for a TAM team report. Keep it concise but comprehensive. Do not use any terminal colors or formatting codes.
        """

        logger.info("Sending request to Amazon Q CLI...")
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        # Call Amazon Q CLI with --no-interactive and --trust-all-tools flags
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', prompt
        ], capture_output=True, text=True, timeout=30)
        
        logger.info(f"Amazon Q CLI completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            # Clean ANSI codes from the output
            raw_output = result.stdout.strip()
            logger.info(f"Raw output length: {len(raw_output)} characters")
            
            cleaned_output = clean_ansi_codes(raw_output)
            logger.info(f"Cleaned output length: {len(cleaned_output)} characters")
            
            # Save the AI summary to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = f"ai_summary_{timestamp}.md"
            try:
                with open(summary_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_output)
                logger.info(f"AI summary saved to {summary_file}")
            except Exception as e:
                logger.warning(f"Could not save summary to file: {e}")
            
            # If the output is still messy, provide a fallback
            if len(cleaned_output) < 50 or '[' in cleaned_output[:100]:
                logger.warning("Output appears to contain formatting issues")
                return False, "Output formatting issue detected. Please check the log file for details."
            
            logger.info("AI summary generated successfully")
            return True, cleaned_output
        else:
            error_msg = result.stderr.strip()
            logger.error(f"Amazon Q CLI error: {error_msg}")
            
            if "not logged in" in error_msg.lower():
                return False, "Authentication required. Please login to Amazon Q CLI."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return False, "Amazon Q usage limit reached. Please try again later."
            else:
                return False, f"Amazon Q error: {clean_ansi_codes(error_msg)}"
            
    except subprocess.TimeoutExpired:
        logger.error("Amazon Q CLI request timed out")
        return False, "Request timed out. Please try again."
    except FileNotFoundError:
        logger.error("Amazon Q CLI not found")
        return False, "Amazon Q CLI not found. Please ensure it's installed and configured."
    except Exception as e:
        logger.error(f"Error generating AI summary: {str(e)}")
        return False, f"Error generating AI summary: {str(e)}"

def detect_q_cli_commands() -> dict:
    """Detect available Amazon Q CLI commands and their format"""
    try:
        # Check help output to determine command structure
        help_result = subprocess.run(['q', '--help'], capture_output=True, text=True, timeout=5)
        help_text = help_result.stdout.lower()
        
        commands = {
            'login': ['q', 'login'],  # Default to simple commands
            'logout': ['q', 'logout'],
            'test': ['q', 'chat', 'hello']
        }
        
        # Based on the error message, this CLI version uses simple commands
        # Try different command patterns based on help text
        if 'auth' in help_text and 'login' in help_text:
            # Some versions might have both auth subcommand and direct login
            commands['login'] = ['q', 'auth', 'login']
            commands['logout'] = ['q', 'auth', 'logout']
            commands['test'] = ['q', 'chat', '--no-interactive', '--trust-all-tools', 'hello']
        else:
            # Most common pattern based on the error message
            commands['login'] = ['q', 'login']
            commands['logout'] = ['q', 'logout']
            commands['test'] = ['q', 'chat', 'hello']
            
        return commands
        
    except Exception:
        # Default fallback based on observed behavior
        return {
            'login': ['q', 'login'],
            'logout': ['q', 'logout'],
            'test': ['q', 'chat', 'hello']
        }


def amazon_q_login_simple() -> tuple[bool, str]:
    """Simple approach: just provide instructions for manual login"""
    try:
        # Check if Q CLI is installed
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            return False, "Amazon Q CLI not installed. Please install it first."
        
        # Return instructions for manual login
        return False, """📋 Please login manually:

1. Open your terminal/command prompt
2. Run: q login
3. Complete browser authentication
4. Click 'Refresh Status' when done

This is the most reliable method for Amazon Q CLI authentication."""
        
    except FileNotFoundError:
        return False, "Amazon Q CLI not found. Please install it first."
    except Exception as e:
        return False, f"Error: {str(e)}"


def amazon_q_login() -> tuple[bool, str]:
    """Attempt to login to Amazon Q CLI with improved handling"""
    try:
        logger.info("Attempting Amazon Q CLI login...")
        
        # First check if Q CLI is installed
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            return False, "Amazon Q CLI not installed. Please install it first."
        
        # Check if already logged in first
        q_available, q_status = check_amazon_q_availability()
        if q_available:
            return True, "Already logged in! Amazon Q is available."
        
        # For reliability, recommend manual login
        logger.info("Recommending manual login for better reliability")
        return amazon_q_login_simple()
            
    except Exception as e:
        logger.error(f"Error during Amazon Q login: {str(e)}")
        return False, f"Login error: {str(e)}. Please try manual login."


def amazon_q_logout() -> tuple[bool, str]:
    """Logout from Amazon Q CLI"""
    try:
        logger.info("Attempting Amazon Q CLI logout...")
        
        # Detect command format
        commands = detect_q_cli_commands()
        logout_cmd = commands.get('logout')
        
        if not logout_cmd:
            return False, "Unable to determine logout command format. Please logout manually."
        
        logout_result = subprocess.run(logout_cmd, capture_output=True, text=True, timeout=30)
        
        if logout_result.returncode == 0:
            logger.info("Amazon Q CLI logout successful")
            return True, "Logout successful!"
        else:
            error_msg = logout_result.stderr.strip() or logout_result.stdout.strip()
            logger.error(f"Amazon Q CLI logout failed: {error_msg}")
            
            # Provide helpful error message
            if "unrecognized subcommand" in error_msg:
                return False, "Logout command not supported by this Q CLI version. You may need to logout manually or check CLI documentation."
            else:
                return False, f"Logout failed: {error_msg}"
            
    except Exception as e:
        logger.error(f"Error during Amazon Q logout: {str(e)}")
        return False, f"Logout error: {str(e)}"


def check_amazon_q_availability() -> tuple[bool, str]:
    """Check if Amazon Q CLI is available and configured with caching"""
    global _amazon_q_cache
    
    # Check cache first
    current_time = time.time()
    if (_amazon_q_cache['timestamp'] > 0 and 
        current_time - _amazon_q_cache['timestamp'] < _amazon_q_cache['cache_duration']):
        logger.info(f"Using cached Amazon Q status: {_amazon_q_cache['message']}")
        return _amazon_q_cache['status'], _amazon_q_cache['message']
    
    try:
        logger.info("Checking Amazon Q CLI availability...")
        
        # Check if CLI is installed
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            logger.error("Amazon Q CLI not installed")
            result = (False, "Amazon Q CLI not installed")
            _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
            return result
        
        logger.info(f"Amazon Q CLI version: {version_result.stdout.strip()}")
        
        # Use a faster login status check instead of chat command
        try:
            # Method 1: Try login command to check if already logged in (fastest)
            login_check = subprocess.run(['q', 'login'], capture_output=True, text=True, timeout=3)
            stderr_lower = login_check.stderr.lower()
            stdout_lower = login_check.stdout.lower()
            
            if ("already logged in" in stderr_lower or "already logged in" in stdout_lower or
                "you are already authenticated" in stderr_lower or "you are already authenticated" in stdout_lower):
                logger.info("Amazon Q CLI is logged in (detected via login check)")
                result = (True, "Available and authenticated")
                _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
                return result
            
            # Method 2: If login check doesn't show "already logged in", try help command
            help_result = subprocess.run(['q', 'chat', '--help'], capture_output=True, text=True, timeout=3)
            if help_result.returncode == 0:
                # If help works, assume logged in (skip slow chat test)
                logger.info("Help command works, assuming CLI is available")
                result = (True, "Available (help command works)")
                _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
                return result
            else:
                # Help command failed, likely not logged in
                if "not logged in" in help_result.stderr.lower():
                    logger.warning("User not logged in to Amazon Q")
                    result = (False, "Not logged in")
                    _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
                    return result
                else:
                    logger.error(f"Help command failed: {help_result.stderr}")
                    result = (False, f"CLI error: {help_result.stderr[:100]}")
                    _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
                    return result
                    
        except subprocess.TimeoutExpired:
            logger.warning("Login status check timed out, assuming CLI is available")
            result = (True, "Available (status check timed out but CLI detected)")
            _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
            return result
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout checking Amazon Q status")
        result = (False, "Status check timed out")
        _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
        return result
    except FileNotFoundError:
        logger.error("Amazon Q CLI not found")
        result = (False, "Amazon Q CLI not found")
        _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
        return result
    except Exception as e:
        logger.error(f"Error checking Amazon Q: {str(e)}")
        result = (False, f"Error checking Amazon Q: {str(e)}")
        _amazon_q_cache.update({'status': result[0], 'message': result[1], 'timestamp': current_time})
        return result


def clear_amazon_q_cache():
    """Clear the Amazon Q status cache to force a fresh check"""
    global _amazon_q_cache
    _amazon_q_cache['timestamp'] = 0
    logger.info("Amazon Q status cache cleared")





# -------------------------------
# Utility helpers
# -------------------------------

def _first_nonempty_row_as_header(df: pd.DataFrame, search_cols: List[str] = None, start_row: int = 0, end_row: int = 20) -> Tuple[pd.DataFrame, int]:
    """Try to find the header row by scanning a range of rows.
    We look for a row that contains all keywords in `search_cols` (case-insensitive, substring match).
    Returns (cleaned_df, header_row_index_in_original_df)
    """
    search_cols = search_cols or ["Customer", "Security", "Overall"]
    header_idx_found = None
    for i in range(start_row, min(len(df), end_row)):
        row_vals = df.iloc[i].astype(str).fillna("")
        hits = 0
        for key in search_cols:
            if any(key.lower() in str(v).lower() for v in row_vals.values):
                hits += 1
        if hits >= max(2, len(search_cols) - 1):  # heuristic: at least 2 hits
            header_idx_found = i
            break

    if header_idx_found is None:
        # fallback to the provided header row (commonly 3) without changes
        header_idx_found = start_row

    new_df = df.copy()
    new_df.columns = new_df.iloc[header_idx_found].astype(str)
    new_df = new_df.iloc[header_idx_found + 1 :].reset_index(drop=True)
    # drop fully-empty columns
    new_df = new_df.dropna(axis=1, how="all")
    return new_df, header_idx_found


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _normalize_colnames(cols: List[str]) -> List[str]:
    return [re.sub(r"\s+", " ", c).strip() for c in cols]


# -------------------------------
# Category logic
# -------------------------------

def calculate_low_score_metrics(df: pd.DataFrame, col_prev: str, col_curr: str, threshold: float = 42) -> Dict[str, int]:
    """Calculate overall low security score metrics for trend analysis"""
    work = df.copy()
    work[col_prev] = _coerce_numeric(work[col_prev])
    work[col_curr] = _coerce_numeric(work[col_curr])
    
    # Count customers with low scores in previous month (excluding NaN)
    prev_low_count = len(work[(work[col_prev] < threshold) & work[col_prev].notna()])
    
    # Count customers with low scores in current month (excluding NaN)
    curr_low_count = len(work[(work[col_curr] < threshold) & work[col_curr].notna()])
    
    # Calculate improvement metrics
    improvement_count = prev_low_count - curr_low_count
    if prev_low_count > 0:
        improvement_percentage = (improvement_count / prev_low_count) * 100
    else:
        improvement_percentage = 0
    
    return {
        "prev_month_low_total": prev_low_count,
        "curr_month_low_total": curr_low_count,
        "improvement_count": improvement_count,
        "improvement_percentage": improvement_percentage
    }

def classify(df: pd.DataFrame, col_prev: str, col_curr: str, col_overall: str, threshold: float = 42) -> Dict[str, pd.DataFrame]:
    """Classify customers into 4 categories based on previous vs current scores.

    Definitions used:
      - Exit from Red:     prev < threshold  AND curr >= threshold
      - Return Back to Red:prev >= threshold AND curr < threshold
      - New Comer to Red:  prev is NaN       AND curr < threshold
      - Missing from CHI:  Overall Score is NaN (regardless of prev/curr)
    """
    work = df.copy()
    work[col_prev] = _coerce_numeric(work[col_prev])
    work[col_curr] = _coerce_numeric(work[col_curr])
    if col_overall in work.columns:
        work[col_overall] = _coerce_numeric(work[col_overall])
    else:
        work[col_overall] = pd.NA

    exit_from_red = work[(work[col_prev] < threshold) & (work[col_curr] >= threshold)]
    return_back_red = work[(work[col_prev] >= threshold) & (work[col_curr] < threshold)]
    new_comer_red = work[work[col_prev].isna() & (work[col_curr] < threshold)]
    missing_from_chi = work[work[col_overall].isna()]

    return {
        "Exit from Red": exit_from_red,
        "Return Back to Red": return_back_red,
        "New Comer to Red": new_comer_red,
        "Missing from CHI": missing_from_chi,
    }


def summarize_tables(tables: Dict[str, pd.DataFrame], col_customer: str, col_prev: str, col_curr: str) -> pd.DataFrame:
    rows = []
    for cat, dfc in tables.items():
        if dfc is None or dfc.empty:
            continue
        for _, r in dfc[[col_customer, col_prev, col_curr]].fillna("").iterrows():
            rows.append({
                "Category": cat,
                "Customer": r[col_customer],
                "Prev Score": r[col_prev],
                "Curr Score": r[col_curr],
            })
    return pd.DataFrame(rows)


def extract_historical_data(xls: pd.ExcelFile, threshold: float = 42) -> pd.DataFrame:
    """Extract historical trend data from all sheets in the Excel file"""
    historical_data = []
    
    # Get all sheet names and filter for date-like sheets
    sheet_names = [s for s in xls.sheet_names if s != "Sheet1"]
    
    # Sort sheet names to get chronological order
    date_sheets = []
    for sheet in sheet_names:
        try:
            # Try to parse as date (assuming format like "2025-04-07")
            if re.match(r'\d{4}-\d{2}-\d{2}', sheet):
                date_sheets.append((pd.to_datetime(sheet), sheet))
        except:
            continue
    
    # Sort by date
    date_sheets.sort(key=lambda x: x[0])
    
    logger.info(f"Found {len(date_sheets)} dated sheets for trend analysis")
    
    for date_obj, sheet_name in date_sheets:
        try:
            # Load the sheet
            raw_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            sheet_df, _ = _first_nonempty_row_as_header(raw_sheet, start_row=0, end_row=20)
            sheet_df.columns = _normalize_colnames(list(sheet_df.columns))
            
            # Find security score column
            sec_col = None
            for col in sheet_df.columns:
                if re.search(r"security score", col, flags=re.I):
                    sec_col = col
                    break
            
            if sec_col:
                # Calculate metrics for this month
                sheet_df[sec_col] = _coerce_numeric(sheet_df[sec_col])
                low_score_count = len(sheet_df[(sheet_df[sec_col] < threshold) & sheet_df[sec_col].notna()])
                total_customers = len(sheet_df[sheet_df[sec_col].notna()])
                
                historical_data.append({
                    'date': date_obj,
                    'month_label': date_obj.strftime('%Y-%m'),
                    'sheet_name': sheet_name,
                    'low_score_customers': low_score_count,
                    'total_customers': total_customers,
                    'low_score_percentage': (low_score_count / total_customers * 100) if total_customers > 0 else 0
                })
                
                logger.info(f"Processed {sheet_name}: {low_score_count} low-score customers out of {total_customers}")
            
        except Exception as e:
            logger.warning(f"Could not process sheet {sheet_name}: {e}")
            continue
    
    return pd.DataFrame(historical_data)

def calculate_monthly_changes(historical_df: pd.DataFrame, tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calculate month-over-month changes including exits and returns"""
    if len(historical_df) < 2:
        return historical_df
    
    # Add change metrics
    historical_df = historical_df.copy()
    historical_df['exit_from_red'] = 0
    historical_df['return_to_red'] = 0
    historical_df['net_change'] = 0
    
    # Calculate changes for each month (except the first)
    for i in range(1, len(historical_df)):
        prev_count = historical_df.iloc[i-1]['low_score_customers']
        curr_count = historical_df.iloc[i]['low_score_customers']
        net_change = prev_count - curr_count
        
        historical_df.loc[i, 'net_change'] = net_change
        
        # For the latest month, use actual data from classification
        if i == len(historical_df) - 1:
            historical_df.loc[i, 'exit_from_red'] = len(tables.get("Exit from Red", []))
            historical_df.loc[i, 'return_to_red'] = len(tables.get("Return Back to Red", []))
        else:
            # Estimate based on net change (simplified)
            if net_change > 0:
                historical_df.loc[i, 'exit_from_red'] = max(0, net_change)
            else:
                historical_df.loc[i, 'return_to_red'] = max(0, abs(net_change))
    
    return historical_df

def create_trend_chart(historical_df: pd.DataFrame) -> go.Figure:
    """Create a comprehensive trend chart from historical data"""
    
    if historical_df.empty:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No historical data available for trend analysis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
        return fig
    
    # Create the figure
    fig = go.Figure()
    
    # Add Low Score Customers trend line (red)
    fig.add_trace(go.Scatter(
        x=historical_df['month_label'],
        y=historical_df['low_score_customers'],
        mode='lines+markers',
        name='Low Score Customers (<42)',
        line=dict(color='red', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Low Score Customers: %{y}<extra></extra>'
    ))
    
    # Add Exit from Red trend line (green)
    fig.add_trace(go.Scatter(
        x=historical_df['month_label'],
        y=historical_df['exit_from_red'],
        mode='lines+markers',
        name='Exit from Red (Improved)',
        line=dict(color='green', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Exits from Red: %{y}<extra></extra>'
    ))
    
    # Add Return to Red trend line (orange)
    fig.add_trace(go.Scatter(
        x=historical_df['month_label'],
        y=historical_df['return_to_red'],
        mode='lines+markers',
        name='Return Back to Red',
        line=dict(color='orange', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Returns to Red: %{y}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Security Score Historical Trends',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Month',
        yaxis_title='Number of Customers',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        showlegend=True,
        xaxis=dict(tickangle=45)
    )
    
    # Add trend annotations for the latest month
    if len(historical_df) > 1:
        latest = historical_df.iloc[-1]
        previous = historical_df.iloc[-2]
        change = latest['low_score_customers'] - previous['low_score_customers']
        
        fig.add_annotation(
            x=latest['month_label'],
            y=latest['low_score_customers'],
            text=f"Latest: {latest['low_score_customers']} customers<br>Change: {change:+d}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red" if change > 0 else "green",
            bgcolor="white",
            bordercolor="red" if change > 0 else "green"
        )
    
    return fig

def export_excel(tables: Dict[str, pd.DataFrame], summary_df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_df.to_excel(writer, index=False, sheet_name="Summary")
        for name, dfc in tables.items():
            (dfc if not dfc.empty else pd.DataFrame({"Message": ["No records"]})) \
                .to_excel(writer, index=False, sheet_name=name[:31])
    output.seek(0)
    return output.read()


def export_pdf(tables: Dict[str, pd.DataFrame], summary_df: pd.DataFrame, 
               analysis_summary: str = "", ai_summary: str = "", 
               chat_history: List[Tuple[str, str]] = None) -> bytes:
    """Export analysis results to PDF format with rich web-like layout including Amazon Q chat history"""
    if not PDF_AVAILABLE:
        raise ImportError("reportlab is required for PDF export. Install with: pip install reportlab")
    
    output = io.BytesIO()
    
    # Use A4 portrait for better readability
    doc = SimpleDocTemplate(output, pagesize=A4, 
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Enhanced styles matching web layout
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=1,  # Center alignment
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=15,
        alignment=1,
        textColor=colors.grey,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.lightblue,
        borderPadding=5,
        backColor=colors.lightblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=10,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    metric_style = ParagraphStyle(
        'MetricStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=colors.darkred
    )
    
    # Build content with rich layout
    story = []
    
    # Header section
    story.append(Paragraph("🔍 CHI Low Security Score Analysis Report", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary Box
    story.append(Paragraph("📊 Executive Summary", heading_style))
    
    # Calculate key metrics
    total_customers = len(summary_df) if not summary_df.empty else 0
    exit_red_count = len(tables.get('Exit from Red', []))
    return_red_count = len(tables.get('Return Back to Red', []))
    new_red_count = len(tables.get('New Comer to Red', []))
    missing_count = len(tables.get('Missing from CHI', []))
    
    # Key metrics in a highlighted box
    metrics_data = [
        ['📈 Total Customers Analyzed', str(total_customers)],
        ['✅ Customers Exiting Red Zone', f"{exit_red_count} ({(exit_red_count/total_customers*100):.1f}%)" if total_customers > 0 else "0"],
        ['⚠️ Customers Returning to Red', f"{return_red_count} ({(return_red_count/total_customers*100):.1f}%)" if total_customers > 0 else "0"],
        ['🆕 New Customers in Red Zone', f"{new_red_count} ({(new_red_count/total_customers*100):.1f}%)" if total_customers > 0 else "0"],
        ['❓ Missing from CHI', f"{missing_count} ({(missing_count/total_customers*100):.1f}%)" if total_customers > 0 else "0"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[4*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkblue),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.lightblue, colors.white])
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 20))
    
    # Analysis Summary (if provided)
    if analysis_summary:
        story.append(Paragraph("📋 Analysis Summary", heading_style))
        story.append(Paragraph(analysis_summary, normal_style))
        story.append(Spacer(1, 15))
    
    # AI Summary (if available)
    if ai_summary:
        story.append(Paragraph("🤖 AI-Generated Insights", heading_style))
        # Clean and format AI summary with better formatting
        clean_summary = ai_summary.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')
        # Add some styling to the AI summary
        ai_summary_style = ParagraphStyle(
            'AISummary',
            parent=normal_style,
            backColor=colors.lightyellow,
            borderColor=colors.orange,
            borderWidth=1,
            borderPadding=10,
            fontSize=10
        )
        story.append(Paragraph(clean_summary, ai_summary_style))
        story.append(Spacer(1, 20))
    
    # Amazon Q Chat History (if available)
    if chat_history and len(chat_history) > 0:
        story.append(Paragraph("💬 Amazon Q Chat History & Improvements", heading_style))
        
        # Chat history styles
        question_style = ParagraphStyle(
            'ChatQuestion',
            parent=normal_style,
            backColor=colors.lightblue,
            borderColor=colors.blue,
            borderWidth=1,
            borderPadding=8,
            fontSize=9,
            fontName='Helvetica-Bold'
        )
        
        answer_style = ParagraphStyle(
            'ChatAnswer',
            parent=normal_style,
            backColor=colors.lightgrey,
            borderColor=colors.darkgrey,
            borderWidth=1,
            borderPadding=8,
            fontSize=9,
            leftIndent=20
        )
        
        for i, (question, answer) in enumerate(chat_history):
            # Add chat number
            story.append(Paragraph(f"<b>Chat {i+1}:</b>", normal_style))
            story.append(Spacer(1, 5))
            
            # Add question
            clean_question = question.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')
            story.append(Paragraph(f"<b>Question:</b> {clean_question}", question_style))
            story.append(Spacer(1, 5))
            
            # Add answer
            clean_answer = answer.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')
            story.append(Paragraph(f"<b>Amazon Q Response:</b><br/>{clean_answer}", answer_style))
            story.append(Spacer(1, 15))
        
        story.append(Spacer(1, 20))
    
    # Detailed Customer Analysis by Category
    story.append(Paragraph("👥 Detailed Customer Analysis", heading_style))
    
    # Create detailed sections for each category
    category_configs = [
        ('Exit from Red', '✅', colors.green, 'Customers who improved their security scores'),
        ('Return Back to Red', '⚠️', colors.orange, 'Customers whose security scores deteriorated'),
        ('New Comer to Red', '🆕', colors.red, 'New customers with low security scores'),
        ('Missing from CHI', '❓', colors.grey, 'Customers missing from current analysis')
    ]
    
    for category, emoji, color, description in category_configs:
        df = tables.get(category, pd.DataFrame())
        
        # Category header
        story.append(Paragraph(f"{emoji} {category}", subheading_style))
        story.append(Paragraph(description, normal_style))
        
        if not df.empty and 'Customer' in df.columns:
            # Show customer count
            story.append(Paragraph(f"Total customers: {len(df)}", metric_style))
            
            # Create customer table with additional details if available
            customer_data = [['Customer Name']]
            
            # Add score columns if available
            if 'Security Score (Current)' in df.columns:
                customer_data[0].append('Current Score')
            if 'Security Score (Previous)' in df.columns:
                customer_data[0].append('Previous Score')
            if 'Change' in df.columns:
                customer_data[0].append('Change')
            
            # Add customer rows (limit to 20 for space)
            for idx, row in df.head(20).iterrows():
                customer_row = [str(row.get('Customer', 'N/A'))]
                
                if 'Security Score (Current)' in df.columns:
                    current_score = row.get('Security Score (Current)', 'N/A')
                    customer_row.append(f"{current_score:.1f}" if isinstance(current_score, (int, float)) else str(current_score))
                
                if 'Security Score (Previous)' in df.columns:
                    prev_score = row.get('Security Score (Previous)', 'N/A')
                    customer_row.append(f"{prev_score:.1f}" if isinstance(prev_score, (int, float)) else str(prev_score))
                
                if 'Change' in df.columns:
                    change = row.get('Change', 'N/A')
                    if isinstance(change, (int, float)):
                        change_str = f"{change:+.1f}"
                        customer_row.append(change_str)
                    else:
                        customer_row.append(str(change))
                
                customer_data.append(customer_row)
            
            # Show "and X more..." if there are more customers
            if len(df) > 20:
                more_row = [f"... and {len(df) - 20} more customers"] + [''] * (len(customer_data[0]) - 1)
                customer_data.append(more_row)
            
            # Create table
            if len(customer_data) > 1:
                # Calculate column widths
                num_cols = len(customer_data[0])
                if num_cols == 1:
                    col_widths = [6*inch]
                elif num_cols == 2:
                    col_widths = [4*inch, 2*inch]
                elif num_cols == 3:
                    col_widths = [3*inch, 1.5*inch, 1.5*inch]
                else:
                    col_widths = [2.5*inch, 1.2*inch, 1.2*inch, 1.1*inch]
                
                customer_table = Table(customer_data, colWidths=col_widths)
                customer_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), color),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 1), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                ]))
                story.append(customer_table)
        else:
            story.append(Paragraph("No customers in this category", normal_style))
        
        story.append(Spacer(1, 15))
    
    # Add footer
    story.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=normal_style,
        fontSize=8,
        alignment=1,
        textColor=colors.grey
    )
    story.append(Paragraph("Generated by CHI Low Security Score Analyzer", footer_style))
    story.append(Paragraph("For internal use only - Contains confidential customer information", footer_style))
    
    # Build PDF with enhanced layout
    doc.build(story)
    output.seek(0)
    return output.read()


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="CHI Low Security Score Analyzer", layout="wide")
st.title("CHI Low Security Score Analyzer")
st.caption(f"Version {APP_VERSION} | Professional Customer Health Index Analysis Tool")

st.markdown(
    "Upload a monthly CHI Excel and compare two months’ **Security Score** to classify customers into: "
    "**Exit from Red**, **Return Back to Red**, **New Comer to Red**, and **Missing from CHI**."
)

file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"]) 

with st.sidebar:
    st.header("Settings")
    threshold = st.number_input("Red-zone threshold", value=42.0, step=0.5)
    mode = st.radio(
        "Comparison mode",
        ["Sheet1 columns (e.g., Oct vs Sept)", "Two sheets (e.g., 2025-09-08 vs 2025-10-06)"]
    )
    st.caption("Tip: If your Sheet1 has merged headers, we'll auto-detect the header row (often row 6).")
    
    # Amazon Q CLI Management Section
    st.markdown("---")
    st.header("🤖 Amazon Q CLI")
    
    # Add refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Status", help="Check current Amazon Q CLI status"):
            st.rerun()
    
    # Check current status
    q_available, q_status = check_amazon_q_availability()
    
    if q_available:
        st.success(f"✅ Status: {q_status}")
        
        # Logout button
        if st.button("🚪 Logout from Amazon Q", help="Logout from Amazon Q CLI"):
            with st.spinner("Logging out from Amazon Q..."):
                logout_success, logout_message = amazon_q_logout()
                if logout_success:
                    st.success(logout_message)
                    st.rerun()  # Refresh to update status
                else:
                    st.error(logout_message)
    else:
        st.warning(f"⚠️ Status: {q_status}")
        
        # Prominent manual login instructions
        st.info("🔑 **To enable Amazon Q CLI:**")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.code("q login", language="bash")
        with col2:
            if st.button("📋 Copy Command", help="Copy login command"):
                st.success("Command copied!")
        
        st.markdown("""
        **Steps:**
        1. Open your terminal/command prompt
        2. Run the command above: `q login`
        3. Complete authentication in your browser
        4. Click 'Refresh Status' when done
        """)
        
        # Alternative: Try automatic login (less reliable)
        with st.expander("🤖 Try Automatic Login (Experimental)"):
            st.warning("⚠️ Automatic login may hang. Manual login is recommended.")
            if st.button("🔑 Try Automatic Login", help="Attempt automatic login (may require browser)"):
                with st.spinner("Attempting automatic login..."):
                    # Use the simple approach that just gives instructions
                    login_success, login_message = amazon_q_login_simple()
                    if login_success:
                        st.success(login_message)
                        st.rerun()
                    else:
                        st.info(login_message)
        
        # Manual instructions
        with st.expander("📋 Detailed Manual Instructions"):
            st.markdown("""
            **If the automatic login doesn't work, try these steps:**
            
            1. Open your terminal/command prompt
            2. Run the login command:
               ```bash
               q login
               ```
            3. Follow the browser authentication process
            4. Return to this app and click 'Refresh Status'
            
            **Troubleshooting:**
            - Check your Q CLI version: `q --version`
            - View available commands: `q --help`
            - If login hangs, try Ctrl+C and retry
            
            **Installation (if needed):**
            ```bash
            # Linux/Mac
            curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh
            
            # Windows - Follow AWS documentation
            ```
            """)
    
    # Show version and command info if available
    try:
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode == 0:
            st.caption(f"CLI Version: {version_result.stdout.strip()}")
            
            # Show detected commands in debug mode
            if st.checkbox("🔧 Show CLI Commands", help="Show detected CLI command format"):
                commands = detect_q_cli_commands()
                st.json({
                    "Detected Commands": {
                        "Login": " ".join(commands.get('login', ['Unknown'])),
                        "Logout": " ".join(commands.get('logout', ['Unknown'])),
                        "Test": " ".join(commands.get('test', ['Unknown']))
                    }
                })
    except:
        pass

if file:
    try:
        # Load workbook, read Sheet1 as raw (no header) for scanning
        xls = pd.ExcelFile(file)
        raw = pd.read_excel(file, sheet_name="Sheet1", header=None)
        # Heuristic: find header row between 0..20
        scanned, header_row = _first_nonempty_row_as_header(raw, start_row=0, end_row=20)
        scanned.columns = _normalize_colnames(list(scanned.columns))

        # Try to detect common columns
        # We keep and standardize likely column names
        # Customer
        cust_candidates = [c for c in scanned.columns if c.lower().strip() == "customer"]
        if not cust_candidates:
            st.error("Could not find a 'Customer' column on Sheet1. Please ensure your file has it.")
            st.stop()
        col_customer = cust_candidates[0]

        # Overall Score (optional)
        overall_candidates = [c for c in scanned.columns if c.lower().strip() == "overall score"]
        col_overall = overall_candidates[0] if overall_candidates else "Overall Score"
        if col_overall not in scanned.columns:
            scanned[col_overall] = pd.NA

        if mode == "Sheet1 columns (e.g., Oct vs Sept)":
            st.subheader("Mode A — Compare two columns on Sheet1")
            # Let user choose two security columns from Sheet1
            sec_cols = [c for c in scanned.columns if re.search(r"security score", c, flags=re.I)]
            if len(sec_cols) < 2:
                st.error("Could not find at least two 'Security Score' columns on Sheet1.")
                st.stop()
            col_prev = st.selectbox("Previous month column", sec_cols, index=1 if len(sec_cols) > 1 else 0)
            col_curr = st.selectbox("Current month column", sec_cols, index=0)

            # Build working df
            work = scanned[[col_customer, col_overall, col_prev, col_curr]].copy()
            tables = classify(work, col_prev=col_prev, col_curr=col_curr, col_overall=col_overall, threshold=threshold)
            
            # Calculate low score metrics for trend analysis
            low_score_metrics = calculate_low_score_metrics(work, col_prev=col_prev, col_curr=col_curr, threshold=threshold)

        else:
            st.subheader("Mode B — Compare two dated sheets")
            # Let user pick two sheets (prev and curr) from workbook
            sheet_names = [s for s in xls.sheet_names if s != "Sheet1"]
            if len(sheet_names) < 2:
                st.error("Need at least two dated sheets besides 'Sheet1' to compare.")
                st.stop()
            prev_sheet = st.selectbox("Previous month sheet", sheet_names, index=0)
            curr_sheet = st.selectbox("Current month sheet", sheet_names, index=1 if len(sheet_names) > 1 else 0)

            def load_sheet(sheet: str) -> pd.DataFrame:
                tmp_raw = pd.read_excel(file, sheet_name=sheet, header=None)
                tmp_df, _ = _first_nonempty_row_as_header(tmp_raw, start_row=0, end_row=20)
                tmp_df.columns = _normalize_colnames(list(tmp_df.columns))
                return tmp_df

            df_prev = load_sheet(prev_sheet)
            df_curr = load_sheet(curr_sheet)

            # Find the likely security score column in each sheet
            def find_security_col(cols: List[str]) -> str:
                candidates = [c for c in cols if re.search(r"security score", c, flags=re.I)]
                if not candidates:
                    return None
                # If multiple, pick the first
                return candidates[0]

            prev_sec_col = find_security_col(list(df_prev.columns))
            curr_sec_col = find_security_col(list(df_curr.columns))

            if not prev_sec_col or not curr_sec_col:
                st.error("Could not detect 'Security Score' column in one or both selected sheets.")
                st.stop()

            # Merge by Customer
            for need in [col_customer, col_overall]:
                if need not in df_prev.columns:
                    df_prev[need] = pd.NA
                if need not in df_curr.columns:
                    df_curr[need] = pd.NA

            merged = pd.merge(
                df_prev[[col_customer, prev_sec_col]].rename(columns={prev_sec_col: "Prev"}),
                df_curr[[col_customer, col_overall, curr_sec_col]].rename(columns={curr_sec_col: "Curr"}),
                on=col_customer, how="outer"
            )
            # Reuse classify() by naming columns accordingly
            merged = merged.rename(columns={"Prev": "__prev__", "Curr": "__curr__"})
            tables = classify(merged, col_prev="__prev__", col_curr="__curr__", col_overall=col_overall, threshold=threshold)
            col_prev, col_curr = "__prev__", "__curr__"
            
            # Calculate low score metrics for trend analysis
            low_score_metrics = calculate_low_score_metrics(merged, col_prev="__prev__", col_curr="__curr__", threshold=threshold)

        # Display results
        st.markdown("---")
        
        # Calculate summary statistics
        counts = {k: (0 if v is None else len(v)) for k, v in tables.items()}
        total_customers = sum(counts.values())
        
        # Overall Analysis Summary at the top
        st.subheader("📊 Overall Analysis Summary")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Key Insights:**")
            
            # Calculate percentages
            if total_customers > 0:
                exit_pct = (counts["Exit from Red"] / total_customers) * 100
                return_pct = (counts["Return Back to Red"] / total_customers) * 100
                new_pct = (counts["New Comer to Red"] / total_customers) * 100
                missing_pct = (counts["Missing from CHI"] / total_customers) * 100
                
                # Determine the most significant change
                max_category = max(counts, key=counts.get)
                max_count = counts[max_category]
                
                st.markdown(f"• **Total customers analyzed:** {total_customers}")
                st.markdown(f"• **Largest category:** {max_category} ({max_count} customers, {(max_count/total_customers)*100:.1f}%)")
                
                # Add low score trend metrics
                st.markdown(f"• **📈 Low Score Trend:** {low_score_metrics['prev_month_low_total']} → {low_score_metrics['curr_month_low_total']} customers (<{threshold})")
                if low_score_metrics['improvement_count'] > 0:
                    st.markdown(f"• **🎯 Overall Improvement:** {low_score_metrics['improvement_count']} fewer low-score customers ({low_score_metrics['improvement_percentage']:.1f}% improvement)")
                elif low_score_metrics['improvement_count'] < 0:
                    st.markdown(f"• **⚠️ Overall Concern:** {abs(low_score_metrics['improvement_count'])} more low-score customers ({abs(low_score_metrics['improvement_percentage']):.1f}% increase)")
                else:
                    st.markdown(f"• **➡️ Stable Trend:** No change in total low-score customers")
                
                if counts["Exit from Red"] > 0:
                    st.markdown(f"• **✅ Positive trend:** {counts['Exit from Red']} customers improved (exited red zone)")
                
                if counts["Return Back to Red"] > 0:
                    st.markdown(f"• **⚠️ Attention needed:** {counts['Return Back to Red']} customers deteriorated (returned to red zone)")
                
                if counts["New Comer to Red"] > 0:
                    st.markdown(f"• **🆕 New risks:** {counts['New Comer to Red']} new customers entered red zone")
                
                if counts["Missing from CHI"] > 0:
                    st.markdown(f"• **❓ Data gaps:** {counts['Missing from CHI']} customers missing from CHI system")
            else:
                st.markdown("• No customer data found for analysis")
        
        with col2:
            # Risk level assessment
            st.markdown("**Risk Assessment:**")
            
            if total_customers > 0:
                risk_score = (counts["Return Back to Red"] + counts["New Comer to Red"]) / total_customers
                
                if risk_score > 0.3:
                    st.error("🔴 **High Risk**")
                    st.markdown("Significant number of customers in red zone")
                elif risk_score > 0.15:
                    st.warning("🟡 **Medium Risk**")
                    st.markdown("Moderate attention required")
                else:
                    st.success("🟢 **Low Risk**")
                    st.markdown("Situation under control")
                
                # Improvement ratio
                if counts["Return Back to Red"] + counts["New Comer to Red"] > 0:
                    improvement_ratio = counts["Exit from Red"] / (counts["Return Back to Red"] + counts["New Comer to Red"])
                    st.metric("Improvement Ratio", f"{improvement_ratio:.2f}", 
                             help="Exit from Red / (Return + New Comer)")
        
        st.markdown("---")
        
        # Detailed metrics
        st.subheader("📈 Detailed Metrics")
        
        # Category metrics
        st.markdown("**Category Breakdown:**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Exit from Red", counts["Exit from Red"]) 
        c2.metric("Return Back to Red", counts["Return Back to Red"]) 
        c3.metric("New Comer to Red", counts["New Comer to Red"]) 
        c4.metric("Missing from CHI", counts["Missing from CHI"])
        
        # Trend metrics
        st.markdown("**Low Score Trend Analysis:**")
        t1, t2, t3 = st.columns(3)
        t1.metric("Previous Month Low Score", low_score_metrics['prev_month_low_total'])
        t2.metric("Current Month Low Score", low_score_metrics['curr_month_low_total'], 
                 delta=low_score_metrics['improvement_count'], delta_color="inverse")
        t3.metric("Improvement Rate", f"{low_score_metrics['improvement_percentage']:.1f}%",
                 delta=f"{low_score_metrics['improvement_count']} customers", delta_color="inverse")
        
        # Security Score Trend Chart
        st.markdown("---")
        st.subheader("📈 Security Score Historical Trends")
        
        # Extract historical data from all sheets
        with st.spinner("📊 Analyzing historical trends..."):
            historical_df = extract_historical_data(xls, threshold=threshold)
            
            if not historical_df.empty:
                # Calculate monthly changes
                historical_df = calculate_monthly_changes(historical_df, tables)
                
                # Create and display the trend chart
                fig = create_trend_chart(historical_df)
                st.plotly_chart(fig, width="stretch", config={'displayModeBar': True, 'scrollZoom': True})
                
                # Display historical data table
                with st.expander("📋 View Historical Data"):
                    display_df = historical_df[['month_label', 'low_score_customers', 'exit_from_red', 'return_to_red', 'total_customers']].copy()
                    display_df.columns = ['Month', 'Low Score Customers', 'Exit from Red', 'Return to Red', 'Total Customers']
                    st.dataframe(display_df, width="stretch")
            else:
                st.warning("⚠️ No historical data found. The trend chart requires multiple dated sheets (e.g., '2025-04-07', '2025-05-08') in the Excel file.")
                st.info("💡 **Tip**: Ensure your Excel file contains multiple sheets with date names in YYYY-MM-DD format for historical trend analysis.")
        
        # Add chart insights
        col_insight1, col_insight2 = st.columns(2)
        with col_insight1:
            if low_score_metrics['improvement_count'] > 0:
                st.success(f"📉 **Positive Trend**: {low_score_metrics['improvement_count']} fewer low-score customers")
            elif low_score_metrics['improvement_count'] < 0:
                st.error(f"📈 **Concerning Trend**: {abs(low_score_metrics['improvement_count'])} more low-score customers")
            else:
                st.info("➡️ **Stable Trend**: No change in low-score customer count")
        
        with col_insight2:
            if counts["Exit from Red"] > 0:
                st.success(f"✅ **Success Stories**: {counts['Exit from Red']} customers improved their security posture")
            else:
                st.info("💡 **Opportunity**: Focus on helping customers exit the red zone")

        # Per-category tables
        for name in ["Exit from Red", "Return Back to Red", "New Comer to Red", "Missing from CHI"]:
            st.markdown(f"### {name}")
            dfc = tables[name]
            if dfc is None or dfc.empty:
                st.info("No records")
            else:
                show_cols = [c for c in [col_customer, col_prev, col_curr, col_overall] if c in dfc.columns]
                st.dataframe(dfc[show_cols].rename(columns={col_prev: "Prev Score", col_curr: "Curr Score", col_customer: "Customer", col_overall: "Overall Score"}), width="stretch")

        # Monthly Summary Report
        st.markdown("---")
        st.subheader("📝 Monthly Summary Report")
        
        # Generate dynamic summary based on actual data
        total_current_low = counts["Return Back to Red"] + counts["New Comer to Red"]
        total_previous_low = counts["Return Back to Red"] + counts["Exit from Red"]
        
        if total_previous_low > 0:
            improvement_percentage = ((total_previous_low - total_current_low) / total_previous_low) * 100
        else:
            improvement_percentage = 0
        
        # Check Amazon Q availability silently
        q_available, q_status = check_amazon_q_availability()
        
        # Simple AI Summary button (no complex UI)
        if q_available:
            use_ai = st.button("🤖 Generate AI-Powered Summary", type="primary", 
                              help="Generate intelligent summary using Amazon Q")
        else:
            use_ai = st.button("🤖 Generate AI-Powered Summary", disabled=True, 
                              help=f"Amazon Q not available: {q_status}. Please run 'q login' in terminal.")
            if not q_available:
                st.info(f"💡 **Amazon Q Status**: {q_status}. To enable AI summaries, please run `q login` in your terminal.")
        
        # Generate Summary Report
        st.markdown("---")
        st.subheader("📝 Monthly Summary Report")
        
        # Prepare data for analysis
        analysis_data = {
            'exit_from_red': counts["Exit from Red"],
            'return_back_red': counts["Return Back to Red"],
            'new_comer_red': counts["New Comer to Red"],
            'missing_from_chi': counts["Missing from CHI"],
            'total_customers': total_customers,
            'previous_low': total_previous_low,
            'current_low': total_current_low,
            'improvement_pct': improvement_percentage,
            # New low score trend metrics
            'prev_month_low_total': low_score_metrics['prev_month_low_total'],
            'curr_month_low_total': low_score_metrics['curr_month_low_total'],
            'low_score_improvement_count': low_score_metrics['improvement_count'],
            'low_score_improvement_pct': low_score_metrics['improvement_percentage']
        }
        
        # Standard Monthly Summary Report (Always Show)
        st.markdown("---")
        st.subheader("📝 Standard Monthly Summary Report")
        
        # Generate standard summary text
        summary_text = f"""
        This month's analysis reveals {counts['New Comer to Red']} new customers entering the low security score category and {counts['Return Back to Red']} customers returning to the red zone, requiring immediate attention from their respective TAMs. We congratulate the {counts['Exit from Red']} customers who successfully improved their security posture and exited the low-score category, demonstrating the positive impact of proactive engagement. We encourage all TAMs to maintain their monthly customer security score review practices to sustain this momentum. Overall, the security score landscape shows {"an improvement" if low_score_metrics['improvement_percentage'] > 0 else "a change"} with {low_score_metrics['curr_month_low_total']} customers currently in the low-score category compared to {low_score_metrics['prev_month_low_total']} previously, {"reflecting a " + f"{low_score_metrics['improvement_percentage']:.0f}%" + " improvement" if low_score_metrics['improvement_percentage'] > 0 else "indicating areas for continued focus"}. This progress reflects the effectiveness of TAM collaboration with customers in addressing security concerns. We encourage all TAMs to continue their excellent practice of monthly security score reviews, with particular attention to customers who are new to or returning to the red zone, helping them implement effective measures to enhance their security posture. Additionally, we extend our congratulations to customers who have successfully moved out of the low-score category and encourage continued support to help them maintain strong security practices.
        """
        
        st.markdown(summary_text)
        
        # Download button for standard summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="📄 Download Standard Summary",
            data=summary_text,
            file_name=f"chi_standard_summary_{timestamp}.md",
            mime="text/markdown"
        )
        
        # GenAI Monthly Summary Report (Conditional)
        # Show if user clicked generate button OR if we already have a summary
        show_ai_section = (use_ai and q_available) or ("original_ai_summary" in st.session_state and st.session_state.get("ai_summary_generated", False))
        
        if show_ai_section and q_available:
            st.markdown("---")
            st.subheader("🤖 GenAI Monthly Summary Report")
            
            with st.spinner("🤖 Generating AI-powered summary..."):
                # Generate AI summary (returns success status and content)
                # Generate AI summary only once and store in session state
                if "original_ai_summary" not in st.session_state:
                    print("🔍 DEBUG: Generating NEW AI summary...")
                    success, ai_summary = generate_ai_summary(analysis_data)
                    if success:
                        st.session_state.original_ai_summary = ai_summary
                        st.session_state.ai_summary_generated = True
                        print(f"🔍 DEBUG: AI summary generated and cached. Length: {len(ai_summary)} chars")
                        print(f"🔍 DEBUG: AI summary preview: {ai_summary[:200]}...")
                    else:
                        st.session_state.ai_summary_generated = False
                        st.session_state.ai_summary_error = ai_summary
                        print(f"🔍 DEBUG: AI summary generation FAILED: {ai_summary}")
                else:
                    # Use cached AI summary
                    success = st.session_state.ai_summary_generated
                    ai_summary = st.session_state.original_ai_summary if success else st.session_state.ai_summary_error
                    print(f"🔍 DEBUG: Using CACHED AI summary. Success: {success}")
                    print(f"🔍 DEBUG: Cached summary length: {len(ai_summary)} chars")
                    print(f"🔍 DEBUG: Cached summary preview: {ai_summary[:200]}...")
                
                if success:
                    # Check if there's an improved summary in session state
                    display_summary = st.session_state.get('improved_summary', ai_summary)
                    print(f"🔍 DEBUG: Display summary selection:")
                    print(f"🔍 DEBUG: - Has improved_summary: {'improved_summary' in st.session_state}")
                    print(f"🔍 DEBUG: - Using improved: {'improved_summary' in st.session_state}")
                    print(f"🔍 DEBUG: - Display summary length: {len(display_summary)} chars")
                    print(f"🔍 DEBUG: - Display summary preview: {display_summary[:200]}...")
                    
                    # Show which summary is being displayed
                    col_info, col_actions = st.columns([3, 1])
                    
                    with col_info:
                        if 'improved_summary' in st.session_state and st.session_state.improved_summary != ai_summary:
                            st.info("📝 **Showing improved summary** (modified by Amazon Q Chat)")
                        else:
                            st.info("📝 **Showing original AI summary**")
                    
                    with col_actions:
                        if 'improved_summary' in st.session_state and st.session_state.improved_summary != ai_summary:
                            if st.button("🔄 Revert", key="revert_summary", help="Revert to original AI summary"):
                                del st.session_state.improved_summary
                                st.success("✅ Reverted to original summary")
                                st.rerun()
                        
                        if st.button("🔄 Regenerate", key="regenerate_summary", help="Generate a new AI summary"):
                            # Clear all summary-related session state
                            if 'original_ai_summary' in st.session_state:
                                del st.session_state.original_ai_summary
                            if 'improved_summary' in st.session_state:
                                del st.session_state.improved_summary
                            if 'ai_summary_generated' in st.session_state:
                                del st.session_state.ai_summary_generated
                            if 'chat_history' in st.session_state:
                                st.session_state.chat_history = []
                            st.success("✅ Regenerating AI summary...")
                            st.rerun()
                    
                    # Display the summary (original or improved)
                    st.markdown(display_summary)
                    
                    # Add download button for the current summary
                    st.download_button(
                        label="📄 Download Current Summary",
                        data=display_summary,
                        file_name=f"chi_genai_summary_{timestamp}.md",
                        mime="text/markdown"
                    )
                    
                    # Interactive Chat Section for Summary Improvement
                    st.markdown("---")
                    col_title, col_status = st.columns([3, 1])
                    with col_title:
                        st.subheader("💬 Improve Summary with Amazon Q Chat")
                    with col_status:
                        if st.button("🔄", help="Refresh Amazon Q status", key="refresh_q_status"):
                            clear_amazon_q_cache()
                            st.rerun()
                    
                    # Show current status
                    st.caption(f"Amazon Q Status: {q_status}")
                    
                    # Initialize chat history in session state
                    if "chat_history" not in st.session_state:
                        st.session_state.chat_history = []
                        print("🔍 DEBUG: Initialized empty chat_history")
                    else:
                        print(f"🔍 DEBUG: Chat history has {len(st.session_state.chat_history)} items")
                    
                    # Initialize pending quick question state
                    if "pending_quick_question" not in st.session_state:
                        st.session_state.pending_quick_question = None
                        print("🔍 DEBUG: Initialized pending_quick_question as None", flush=True)
                    else:
                        print(f"🔍 DEBUG: *** FOUND PENDING QUESTION: {st.session_state.pending_quick_question} ***", flush=True)
                    
                    # Prepare context for chat using the currently displayed summary
                    current_displayed_summary = st.session_state.get('improved_summary', ai_summary)
                    
                    def get_chat_context():
                        """Get the current context for Amazon Q chat"""
                        current_summary = st.session_state.get('improved_summary', st.session_state.get('original_ai_summary', ai_summary))
                        print(f"🔍 DEBUG: get_chat_context() called")
                        print(f"🔍 DEBUG: - improved_summary exists: {'improved_summary' in st.session_state}")
                        print(f"🔍 DEBUG: - original_ai_summary exists: {'original_ai_summary' in st.session_state}")
                        print(f"🔍 DEBUG: - current_summary length: {len(current_summary)} chars")
                        print(f"🔍 DEBUG: - current_summary preview: {current_summary[:200]}...")
                        
                        # Truncate summary if too long to avoid timeout
                        summary_for_context = current_summary
                        if len(current_summary) > 2000:
                            summary_for_context = current_summary[:2000] + "\n\n[Summary truncated for processing efficiency]"
                            print(f"🔍 DEBUG: Truncated summary from {len(current_summary)} to {len(summary_for_context)} chars")
                        
                        context = f"""CHI Analysis: {analysis_data['exit_from_red']} improved, {analysis_data['return_back_red']} deteriorated, {analysis_data['new_comer_red']} new low-score, {analysis_data['missing_from_chi']} missing data. Total: {analysis_data['total_customers']} customers, {analysis_data['low_score_improvement_pct']:.1f}% improvement.

Current Summary:
{summary_for_context}"""
                        
                        print(f"🔍 DEBUG: Generated context length: {len(context)} chars")
                        return context
                    
                    # Display chat history
                    if st.session_state.chat_history:
                        st.markdown("**Chat History:**")
                        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
                            with st.expander(f"💬 Chat {i+1}: {user_msg[:50]}..."):
                                st.markdown(f"**You:** {user_msg}")
                                st.markdown(f"**Amazon Q:** {ai_response}")
                    
                    # Chat input
                    st.markdown("**Ask Amazon Q to improve or modify the summary:**")
                    
                    # Predefined quick questions
                    st.markdown("**Quick Actions:**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📈 Focus on improvements", help="Emphasize positive trends", key="btn_improvements"):
                            question = "Please rewrite the summary to focus more on the positive improvements and success stories. Highlight the customers who improved their security scores."
                            st.session_state.pending_quick_question = question
                            print(f"🔍 DEBUG: BUTTON CLICKED - Focus on improvements", flush=True)
                            print(f"🔍 DEBUG: Set pending_quick_question: {question}", flush=True)
                            print(f"🔍 DEBUG: About to call st.rerun()", flush=True)
                            import sys
                            sys.stdout.flush()
                            st.rerun()
                    with col2:
                        if st.button("⚠️ Highlight risks", help="Emphasize areas of concern", key="btn_risks"):
                            st.session_state.pending_quick_question = "Please rewrite the summary to emphasize the security risks and areas that need immediate attention. Focus on the deteriorating customers."
                            st.rerun()
                    with col3:
                        if st.button("📊 Add more metrics", help="Include additional analysis", key="btn_metrics"):
                            st.session_state.pending_quick_question = "Please enhance the summary with more detailed metrics and statistical analysis. Include percentages and trends."
                            st.rerun()
                    
                    # Handle pending quick question
                    if st.session_state.pending_quick_question:
                        print(f"🔍 DEBUG: *** PROCESSING PENDING QUESTION ***", flush=True)
                        quick_question = st.session_state.pending_quick_question
                        print(f"🔍 DEBUG: Question: {quick_question}", flush=True)
                        st.session_state.pending_quick_question = None  # Clear it immediately
                        print(f"🔍 DEBUG: Cleared pending_quick_question", flush=True)
                        
                        with st.spinner("🤖 Getting response from Amazon Q..."):
                            # Use the current context with the displayed summary
                            print(f"🔍 DEBUG: About to call get_chat_context()")
                            context = get_chat_context()
                            print(f"🔍 DEBUG: Context generated, calling chat_with_amazon_q()")
                            print(f"🔍 DEBUG: Context preview: {context[:300]}...")
                            chat_success, chat_response = chat_with_amazon_q(quick_question, context)
                            print(f"🔍 DEBUG: chat_with_amazon_q returned: success={chat_success}")
                            print(f"🔍 DEBUG: Response length: {len(chat_response) if chat_response else 0} chars")
                            
                            if chat_success:
                                print(f"🔍 DEBUG: Chat SUCCESS - adding to history")
                                # Add to chat history
                                st.session_state.chat_history.append((quick_question, chat_response))
                                print(f"🔍 DEBUG: Chat history now has {len(st.session_state.chat_history)} items")
                                
                                # Display the response
                                st.success("✅ Response received!")
                                st.markdown("**Amazon Q Response:**")
                                st.markdown(chat_response)
                                
                                # Option to replace original summary (without rerun)
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("🔄 Use this as new summary", key="replace_summary_quick"):
                                        print(f"🔍 DEBUG: USER CLICKED 'Use this as new summary'")
                                        st.session_state.improved_summary = chat_response
                                        print(f"🔍 DEBUG: Set improved_summary, length: {len(chat_response)} chars")
                                        st.success("✅ Summary updated! The new summary will be used in exports.")
                                        st.rerun()
                                with col_b:
                                    if st.button("📋 Copy to clipboard", key="copy_quick"):
                                        st.success("✅ Response copied! You can paste it elsewhere.")
                                
                            else:
                                print(f"🔍 DEBUG: Chat FAILED: {chat_response}")
                                st.error(f"Chat failed: {chat_response}")
                                if "not logged in" in chat_response.lower():
                                    st.info("💡 **Please login to Amazon Q CLI:**")
                                    st.code("q login")
                                    st.info("Then refresh this page or click the refresh button above.")
                    
                    # Custom question input
                    st.markdown("**Custom Question:**")
                    user_question = st.text_area(
                        "Ask your own question:",
                        placeholder="e.g., 'Make the summary more executive-friendly' or 'Add specific recommendations for TAMs'",
                        key="chat_input"
                    )
                    
                    if st.button("💬 Send Custom Question", type="primary", key="btn_custom") and user_question:
                        st.session_state.pending_custom_question = user_question
                        st.rerun()
                    
                    # Handle pending custom question
                    if "pending_custom_question" not in st.session_state:
                        st.session_state.pending_custom_question = None
                    
                    if st.session_state.pending_custom_question:
                        custom_question = st.session_state.pending_custom_question
                        st.session_state.pending_custom_question = None  # Clear it immediately
                        
                        with st.spinner("🤖 Getting response from Amazon Q..."):
                            # Use the current context with the displayed summary
                            chat_success, chat_response = chat_with_amazon_q(custom_question, get_chat_context())
                            
                            if chat_success:
                                # Add to chat history
                                st.session_state.chat_history.append((custom_question, chat_response))
                                
                                # Display the response
                                st.success("✅ Response received!")
                                st.markdown("**Amazon Q Response:**")
                                st.markdown(chat_response)
                                
                                # Option to replace original summary (without rerun)
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("🔄 Use this as new summary", key="replace_summary_custom"):
                                        st.session_state.improved_summary = chat_response
                                        st.success("✅ Summary updated! The new summary will be used in exports.")
                                        st.rerun()
                                with col_b:
                                    if st.button("📋 Copy to clipboard", key="copy_custom"):
                                        st.success("✅ Response copied! You can paste it elsewhere.")
                                
                            else:
                                st.error(f"Chat failed: {chat_response}")
                                if "not logged in" in chat_response.lower():
                                    st.info("💡 **Please login to Amazon Q CLI:**")
                                    st.code("q login")
                                    st.info("Then refresh this page or click the refresh button above.")
                    
                    # Clear chat history button
                    if st.session_state.chat_history:
                        if st.button("🗑️ Clear Chat History"):
                            st.session_state.chat_history = []
                            # Don't use st.rerun() here, just clear the history
                    
                else:
                    # Show error message
                    st.error(f"AI Summary Generation Failed: {ai_summary}")
                    st.info("Please check the log file for detailed error information.")
        
        elif not q_available:
            st.markdown("---")
            st.subheader("🤖 GenAI Monthly Summary Report")
            st.info("💡 **GenAI Summary Not Available**: Amazon Q CLI is not available or not logged in. Please run `q login` in your terminal to enable AI-powered summaries.")
            st.caption(f"Status: {q_status}")
            
            # Add refresh button to recheck Amazon Q status
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🔄 Recheck Amazon Q", help="Clear cache and recheck Amazon Q CLI status"):
                    clear_amazon_q_cache()
                    st.rerun()
            with col2:
                st.caption("Click to refresh Amazon Q CLI status after login")
            
            # Show chat interface even when not logged in (with disabled state)
            st.markdown("---")
            st.subheader("💬 Amazon Q Chat (Unavailable)")
            st.info("💡 **Chat Feature**: Login to Amazon Q CLI to enable interactive chat for improving summaries.")
            st.text_area("Chat would appear here...", disabled=True, placeholder="Login to Amazon Q CLI to enable chat functionality")

        # Create combined summary for export (keeping original format for Excel)
        summary_df = summarize_tables(tables, col_customer=col_customer, col_prev=col_prev, col_curr=col_curr)
        
        # Export section
        st.markdown("---")
        st.subheader("📥 Export Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Excel Export
            report_bytes = export_excel(tables, summary_df)
            st.download_button(
                label="📊 Download Excel Report",
                data=report_bytes,
                file_name="CHI_Low_Security_Analysis_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        
        with col2:
            # PDF Export - 實時檢測 reportlab
            try:
                from reportlab.lib.pagesizes import A4, landscape
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                pdf_available_now = True
            except ImportError:
                pdf_available_now = False
            
            # 顯示調試資訊
            st.caption(f"🔍 DEBUG: PDF_AVAILABLE={PDF_AVAILABLE}, pdf_available_now={pdf_available_now}")
            
            if pdf_available_now:
                try:
                    # Get AI summary if available (use improved version if exists)
                    ai_summary_text = ""
                    if use_ai and q_available and 'ai_summary' in locals():
                        if success:
                            # Use improved summary if available, otherwise use original
                            ai_summary_text = st.session_state.get('improved_summary', ai_summary)
                        else:
                            ai_summary_text = ""
                    
                    # Get chat history if available
                    chat_history_for_pdf = st.session_state.get('chat_history', [])
                    
                    pdf_bytes = export_pdf(tables, summary_df, 
                                         analysis_summary=summary_text,
                                         ai_summary=ai_summary_text,
                                         chat_history=chat_history_for_pdf)
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name="CHI_Low_Security_Analysis_Report.pdf",
                        mime="application/pdf",
                    )
                except Exception as pdf_error:
                    st.error(f"PDF generation failed: {str(pdf_error)}")
                    st.info("Please ensure reportlab is installed: `pip install reportlab`")
            else:
                st.error("📄 PDF Export unavailable")
                st.caption("Install reportlab to enable PDF export: `pip install reportlab`")
                st.caption("🔧 Try: `chi_analyzer_env/bin/pip install reportlab`")

    except Exception as e:
        st.exception(e)
        st.error("Parsing failed. Please verify sheet layout and column names, or try the other comparison mode.")
