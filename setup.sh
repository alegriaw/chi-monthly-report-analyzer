#!/bin/bash

# CHI Low Security Score Analyzer Setup Script

echo "🚀 Setting up CHI Low Security Score Analyzer..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12.3 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "chi_analyzer_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv chi_analyzer_env
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source chi_analyzer_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python -c "import streamlit, pandas, openpyxl, plotly; print('✅ Core dependencies installed successfully')"

# Check reportlab
python -c "import reportlab; print('✅ ReportLab installed - Enhanced PDF export available')" 2>/dev/null || echo "⚠️ ReportLab not found - PDF export will be basic"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment: source chi_analyzer_env/bin/activate"
echo "2. Run the application: streamlit run chi_low_security_score_analyzer.py"
echo "3. Open your browser to: http://localhost:8501"
echo ""
echo "For Amazon Q CLI integration:"
echo "1. Install Amazon Q CLI (GitHub method):"
echo "   curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
echo "   chmod +x q && sudo mv q /usr/local/bin/"
echo "2. Login: q login"
echo "3. Test: q chat 'hello'"
echo "4. Official docs: https://docs.aws.amazon.com/zh_tw/amazonq/latest/qdeveloper-ug/command-line-installing.html"