#!/usr/bin/env python3
"""
Version checker for CHI Low Security Score Analyzer
"""

import sys
import os

# Add current directory to path to import version module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from version import __version__, __version_info__, VERSION_HISTORY
    
    print("🔍 CHI Low Security Score Analyzer - Version Information")
    print("=" * 55)
    print(f"Current Version: {__version__}")
    print(f"Version Info: {__version_info__}")
    print()
    
    if __version__ in VERSION_HISTORY:
        history = VERSION_HISTORY[__version__]
        print(f"Release Date: {history['release_date']}")
        print(f"Description: {history['description']}")
        print()
        print("Features:")
        for feature in history['features']:
            print(f"  • {feature}")
    
    print()
    print("📋 Dependencies Status:")
    
    # Check core dependencies
    dependencies = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('openpyxl', 'OpenPyXL'),
        ('plotly', 'Plotly'),
        ('reportlab', 'ReportLab (PDF Export)')
    ]
    
    for module_name, display_name in dependencies:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'Unknown')
            print(f"  ✅ {display_name}: {version}")
        except ImportError:
            if module_name == 'reportlab':
                print(f"  ⚠️  {display_name}: Not installed (PDF export unavailable)")
            else:
                print(f"  ❌ {display_name}: Not installed (REQUIRED)")
    
    print()
    print("🚀 To start the application:")
    print("   streamlit run chi_low_security_score_analyzer.py")
    
except ImportError:
    print("❌ Error: version.py not found or invalid")
    print("Please ensure you're running this from the project directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error checking version: {e}")
    sys.exit(1)