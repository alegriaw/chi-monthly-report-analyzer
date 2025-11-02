#!/bin/bash

# CHI Low Security Score Analyzer - WSL Deployment Script
# This script ensures the application always runs in WSL environment

echo "🐧 CHI Low Security Score Analyzer - WSL Deployment"
echo "=================================================="

# Check if running in WSL
if [[ ! -f /proc/version ]] || ! grep -qi microsoft /proc/version; then
    echo "❌ Error: This script must be run in WSL (Windows Subsystem for Linux)"
    echo "Please open WSL terminal and run this script again."
    exit 1
fi

echo "✅ Running in WSL environment"

# Get the current directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "$PROJECT_DIR/chi_analyzer_env" ]; then
    echo "❌ Virtual environment not found. Please run install.sh first."
    exit 1
fi

echo "✅ Virtual environment found"

# Activate virtual environment
source "$PROJECT_DIR/chi_analyzer_env/bin/activate"

# Check if all dependencies are installed
echo "🔍 Checking dependencies..."
python -c "
import sys
required_packages = ['streamlit', 'pandas', 'openpyxl', 'plotly']
optional_packages = ['reportlab']

missing_required = []
missing_optional = []

for package in required_packages:
    try:
        __import__(package)
        print(f'✅ {package}')
    except ImportError:
        missing_required.append(package)
        print(f'❌ {package} (REQUIRED)')

for package in optional_packages:
    try:
        __import__(package)
        print(f'✅ {package} (optional)')
    except ImportError:
        missing_optional.append(package)
        print(f'⚠️  {package} (optional - PDF export unavailable)')

if missing_required:
    print(f'\\n❌ Missing required packages: {missing_required}')
    print('Please run: pip install ' + ' '.join(missing_required))
    sys.exit(1)

if missing_optional:
    print(f'\\n⚠️  Missing optional packages: {missing_optional}')
    print('For full functionality, run: pip install ' + ' '.join(missing_optional))
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency check failed. Installing missing packages..."
    pip install -r requirements.txt
fi

# Check Amazon Q CLI availability
echo ""
echo "🤖 Checking Amazon Q CLI..."

# Check multiple possible locations
Q_LOCATIONS=(
    "/usr/local/bin/q"
    "$HOME/.local/bin/q"
    "$HOME/bin/q"
    "$(which q 2>/dev/null)"
)

Q_FOUND=false
Q_PATH=""

for location in "${Q_LOCATIONS[@]}"; do
    if [ -n "$location" ] && [ -x "$location" ]; then
        Q_FOUND=true
        Q_PATH="$location"
        break
    fi
done

if [ "$Q_FOUND" = true ]; then
    Q_VERSION=$($Q_PATH --version 2>/dev/null || echo "Unknown")
    echo "✅ Amazon Q CLI found at: $Q_PATH"
    echo "   Version: $Q_VERSION"
    
    # Quick login status check with timeout
    echo "🔍 Checking authentication status..."
    if timeout 10s $Q_PATH chat "hello" &>/dev/null; then
        echo "✅ Amazon Q CLI is authenticated and working"
    else
        echo "⚠️  Amazon Q CLI authentication issue or timeout"
        echo "💡 To enable AI features:"
        echo "   1. Run: $Q_PATH login"
        echo "   2. Complete browser authentication"
        echo "   3. Test with: $Q_PATH chat 'hello'"
    fi
else
    echo "⚠️  Amazon Q CLI not found"
    echo ""
    echo "📖 根據 AWS 官方文件，Amazon Q CLI 安裝方法："
    echo "   官方文件: https://docs.aws.amazon.com/zh_tw/amazonq/latest/qdeveloper-ug/command-line-installing.html"
    echo ""
    echo "🔧 WSL/Linux 安裝步驟 (根據 AWS 官方 blog)："
    echo ""
    echo "   方法 1 - 直接下載二進位檔案 (推薦):"
    echo "     # 下載最新版本"
    echo "     curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
    echo "     chmod +x q"
    echo "     sudo mv q /usr/local/bin/"
    echo ""
    echo "   方法 2 - 使用 wget:"
    echo "     wget https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
    echo "     chmod +x q-linux-amd64"
    echo "     sudo mv q-linux-amd64 /usr/local/bin/q"
    echo ""
    echo "   方法 3 - 安裝到用戶目錄 (無需 sudo):"
    echo "     mkdir -p ~/.local/bin"
    echo "     curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
    echo "     chmod +x ~/.local/bin/q"
    echo "     echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "     source ~/.bashrc"
    echo ""
    echo "   方法 4 - 從 AWS 控制台下載:"
    echo "     1. 登入 AWS 控制台"
    echo "     2. 搜尋 'Amazon Q Developer'"
    echo "     3. 下載 CLI 工具"
    echo ""
    echo "💡 安裝後的設定步驟："
    echo "   1. 驗證安裝: q --version"
    echo "   2. 登入認證: q login"
    echo "   3. 測試連接: q chat 'hello'"
    echo ""
    
    # Ask user what they want to do
    echo "選擇操作:"
    echo "  1) 嘗試自動安裝 Amazon Q CLI"
    echo "  2) 運行網路診斷工具"
    echo "  3) 跳過，稍後手動安裝"
    echo ""
    read -p "請選擇 (1/2/3): " -n 1 -r
    echo
    
    if [[ $REPLY == "1" ]]; then
        echo "📥 正在安裝 Amazon Q CLI..."
        
        # Try multiple installation methods based on the blog guide
        echo "🔄 嘗試方法 1: 從 GitHub 直接下載..."
        if curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null && chmod +x q && sudo mv q /usr/local/bin/ 2>/dev/null; then
            echo "✅ Amazon Q CLI 安裝完成"
            
            # Reload shell configuration
            if [ -f ~/.bashrc ]; then
                source ~/.bashrc
            fi
            
            # Check if q is now available
            if command -v q &> /dev/null; then
                Q_VERSION=$(q --version 2>/dev/null || echo "Unknown")
                echo "✅ 安裝驗證成功: $Q_VERSION"
                echo "💡 請執行 'q login' 進行認證"
            else
                echo "⚠️  安裝完成但 q 命令不在 PATH 中"
                echo "💡 請執行以下命令："
                echo "   source ~/.bashrc"
                echo "   q --version"
            fi
        else
            echo "⚠️  方法 1 失敗，嘗試用戶目錄安裝..."
            
            # Try installing to user directory (no sudo required)
            mkdir -p ~/.local/bin
            if curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null && chmod +x ~/.local/bin/q; then
                echo "✅ 安裝到用戶目錄成功"
                
                # Add to PATH if not already there
                if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
                    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
                    export PATH="$HOME/.local/bin:$PATH"
                    echo "✅ 已添加到 PATH"
                fi
            elif command -v wget &> /dev/null; then
                echo "🔄 嘗試使用 wget..."
                if wget -O ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null && chmod +x ~/.local/bin/q; then
                    echo "✅ 使用 wget 安裝成功"
                    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
                        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
                        export PATH="$HOME/.local/bin:$PATH"
                    fi
                else
                    echo "❌ wget 方法也失敗"
                fi
            else
                echo "❌ 自動安裝失敗"
            fi
            
            echo ""
            echo "🔧 手動安裝選項："
            echo "   選項 1 - 從 AWS 控制台下載:"
            echo "     1. 登入 AWS 控制台"
            echo "     2. 搜尋 'Amazon Q'"
            echo "     3. 下載 CLI 工具"
            echo ""
            echo "   選項 2 - 網路問題排解:"
            echo "     1. 檢查網路連接: ping amazon.com"
            echo "     2. 檢查 DNS: nslookup d2yblsmsllhwuq.cloudfront.net"
            echo "     3. 嘗試使用代理或 VPN"
            echo ""
            echo "   選項 3 - 企業環境:"
            echo "     1. 聯繫 IT 部門關於防火牆設定"
            echo "     2. 請求允許訪問 *.cloudfront.net"
        fi
    elif [[ $REPLY == "2" ]]; then
        echo "🔍 運行網路診斷工具..."
        if [ -f "diagnose-network.sh" ]; then
            bash diagnose-network.sh
        else
            echo "❌ 診斷工具不存在，請手動檢查網路連接"
            echo ""
            echo "🔧 快速診斷命令:"
            echo "   ping -c 3 amazon.com"
            echo "   nslookup d2yblsmsllhwuq.cloudfront.net"
            echo "   curl -I https://d2yblsmsllhwuq.cloudfront.net"
        fi
    else
        echo "💡 您可以稍後手動安裝 Amazon Q CLI"
        echo "   參考: https://docs.aws.amazon.com/zh_tw/amazonq/latest/qdeveloper-ug/command-line-installing.html"
        echo "   網路問題排解: bash diagnose-network.sh"
    fi
fi

# Get WSL IP address for network access
WSL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "🌐 Network Information:"
echo "   Local URL: http://localhost:8501"
echo "   WSL IP URL: http://$WSL_IP:8501"
echo "   Network URL: http://$(hostname):8501"

# Kill any existing Streamlit processes
echo ""
echo "🔄 Checking for existing Streamlit processes..."
if pgrep -f "streamlit.*chi_low_security_score_analyzer.py" > /dev/null; then
    echo "⚠️  Found existing Streamlit processes. Stopping them..."
    pkill -f "streamlit.*chi_low_security_score_analyzer.py"
    sleep 2
fi

# Start the application
echo ""
echo "🚀 Starting CHI Low Security Score Analyzer..."
echo "   Press Ctrl+C to stop the application"
echo "   Application will be available at: http://localhost:8501"
echo ""

# Start Streamlit with WSL-optimized settings
exec streamlit run chi_low_security_score_analyzer.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false