#!/bin/bash

# CHI Low Security Score Analyzer Installation Script
# This script sets up the virtual environment and installs all dependencies

echo "🚀 CHI Low Security Score Analyzer v2.0.2 Installation"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv chi_analyzer_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source chi_analyzer_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment:"
echo "   source chi_analyzer_env/bin/activate"
echo ""
echo "2. Start the application:"
echo "   streamlit run chi_low_security_score_analyzer.py"
echo ""
echo "3. Open your browser to: http://localhost:8501"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "🔧 Optional: Install Amazon Q CLI for AI features:"
echo "   curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
echo "   chmod +x q && sudo mv q /usr/local/bin/ && q login"