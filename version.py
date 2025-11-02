"""
CHI Low Security Score Analyzer Version Information
"""

__version__ = "2.0.7"
__version_info__ = (2, 0, 7)

# Version history
VERSION_HISTORY = {
    "2.0.7": {
        "release_date": "2025-11-03",
        "description": "Comprehensive technical documentation for GenAI report and Amazon Q CLI session management mechanisms",
        "features": [
            "Added comprehensive GenAI Report & Amazon Q CLI Session Management documentation",
            "Detailed state management architecture documentation with multi-layered persistence",
            "Complete AI summary generation control and caching mechanism documentation",
            "Amazon Q CLI session management and multi-turn conversation documentation",
            "Button interaction processing and UI state management technical guide",
            "Error handling, recovery strategies, and performance optimization documentation",
            "Debug monitoring and troubleshooting procedures comprehensive guide",
            "Enhanced README.md with organized technical documentation section",
            "Updated documentation status reflecting complete technical architecture coverage"
        ]
    },
    "2.0.6": {
        "release_date": "2025-11-02",
        "description": "Enhanced debugging and logging for AI summary generation and caching, with improved debug output flushing for better visibility",
        "features": [
            "Enhanced debug logging with explicit flushing for immediate visibility",
            "Improved debug output for button interactions with sys.stdout.flush()",
            "Better debugging visibility for AI summary generation and caching behavior",
            "Enhanced debug messages for pending question handling and session state management",
            "Comprehensive debug output with flush=True parameters for real-time feedback",
            "Improved troubleshooting capabilities with immediate debug message display",
            "Enhanced logging for AI summary lifecycle tracking and caching decisions",
            "Better visibility into session state changes and button click handling"
        ]
    },
    "2.0.5": {
        "release_date": "2025-11-02",
        "description": "AI summary caching and performance optimization for improved user experience",
        "features": [
            "AI summary caching with original_ai_summary session state storage",
            "Performance enhancement through single-generation AI summary reuse",
            "Improved user experience eliminating regeneration wait times",
            "Enhanced session state management with ai_summary_generated flags",
            "Better error handling with persistent error state management",
            "Memory efficiency through reduced Amazon Q CLI API calls",
            "Intelligent caching mechanism preventing unnecessary regeneration",
            "Optimized session state variables for better performance"
        ]
    },
    "2.0.4": {
        "release_date": "2025-11-02",
        "description": "Enhanced chat interface session management for improved user experience",
        "features": [
            "Improved session state handling with pending_quick_question management",
            "AI summary persistence through current_ai_summary session state storage",
            "Enhanced quick question button reliability without summary resets",
            "Better state management with immediate clearing to prevent conflicts",
            "Data preservation during chat sessions eliminating regeneration needs",
            "Seamless user experience with optimized session state variables",
            "Enhanced protection against accidental data loss during interactions",
            "Performance improvements through reduced AI summary regeneration"
        ]
    },
    "2.0.3": {
        "release_date": "2025-11-02",
        "description": "Enhanced Amazon Q CLI authentication with optimized multi-layered detection",
        "features": [
            "Optimized authentication detection with multi-layered status checking",
            "Faster status verification using login command instead of chat tests",
            "Staged timeout approach: 5s login check, 3s help validation, 8s chat test",
            "Enhanced resilience to network issues and partial failures",
            "Improved user experience with detailed authentication status reporting",
            "Performance optimization reducing authentication check time significantly",
            "Better error classification and resolution guidance",
            "Enhanced logging and debugging information for authentication issues"
        ]
    },
    "2.0.2": {
        "release_date": "2025-10-17",
        "description": "Documentation improvements and technology stack updates",
        "features": [
            "Enhanced README.md with comprehensive technology stack information",
            "Added license section for internal use guidelines",
            "Improved development environment documentation",
            "Updated dependency information and installation instructions",
            "Consistent documentation formatting across all files",
            "Comprehensive documentation review and validation"
        ]
    },
    "2.0.1": {
        "release_date": "2025-10-16",
        "description": "Enhanced chart interactivity with full control toolbar",
        "features": [
            "Interactive chart controls with zoom, pan, and selection tools",
            "Scroll zoom functionality for detailed data exploration", 
            "Built-in chart export options (PNG, SVG, PDF)",
            "Enhanced user experience with professional chart interactions",
            "Improved trend analysis visualization capabilities"
        ]
    },
    "2.0.0": {
        "release_date": "2025-10-16",
        "description": "Major update with enhanced AI features, historical trend analysis, and professional reporting",
        "features": [
            "Interactive Amazon Q chat interface with context awareness",
            "Multi-turn conversations and chat history management",
            "Historical trend analysis across multiple dated sheets",
            "Interactive Plotly trend charts with hover details",
            "Enhanced AI summary generation with professional formatting",
            "Advanced risk assessment dashboard with color-coded indicators",
            "Professional PDF reports with rich visual design and AI insights",
            "Improved Amazon Q CLI integration with smart error handling",
            "Real-time metrics and improvement percentage calculations",
            "Graceful degradation for optional dependencies"
        ]
    },
    "1.0.0": {
        "release_date": "2025-10-15",
        "description": "Initial stable release with enhanced PDF export functionality",
        "features": [
            "Excel data processing and analysis",
            "Customer classification into four categories", 
            "Enhanced PDF reports with professional formatting",
            "Amazon Q CLI integration for AI summaries",
            "Trend analysis and visualization",
            "Streamlit web interface"
        ]
    }
}

def get_version():
    """Return the current version string."""
    return __version__

def get_version_info():
    """Return the current version as a tuple."""
    return __version_info__