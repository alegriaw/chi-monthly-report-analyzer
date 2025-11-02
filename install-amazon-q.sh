#!/bin/bash

echo "🤖 Amazon Q CLI 安裝工具 - WSL/Linux"
echo "=================================="

# 檢查是否已安裝
if command -v q &> /dev/null; then
    Q_VERSION=$(q --version 2>/dev/null || echo "Unknown")
    echo "✅ Amazon Q CLI 已安裝: $Q_VERSION"
    echo "💡 如需重新安裝，請先執行: sudo rm /usr/local/bin/q"
    exit 0
fi

echo "📥 開始安裝 Amazon Q CLI..."

# 方法 1: GitHub 直接下載 (推薦)
echo "🔄 方法 1: 從 GitHub 下載最新版本..."
if curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null; then
    chmod +x q
    if sudo mv q /usr/local/bin/ 2>/dev/null; then
        echo "✅ 安裝成功到 /usr/local/bin/"
        Q_VERSION=$(q --version 2>/dev/null || echo "Unknown")
        echo "✅ 版本: $Q_VERSION"
        
        echo ""
        echo "🔐 下一步: 執行認證"
        echo "   q login"
        echo ""
        echo "🧪 測試連接:"
        echo "   q chat 'hello'"
        exit 0
    else
        echo "⚠️  需要 sudo 權限，嘗試用戶目錄安裝..."
        rm -f q
    fi
fi

# 方法 2: 用戶目錄安裝 (無需 sudo)
echo "🔄 方法 2: 安裝到用戶目錄..."
mkdir -p ~/.local/bin

if curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null; then
    chmod +x ~/.local/bin/q
    
    # 添加到 PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        export PATH="$HOME/.local/bin:$PATH"
        echo "✅ 已添加 ~/.local/bin 到 PATH"
    fi
    
    echo "✅ 安裝成功到 ~/.local/bin/"
    
    # 重新載入 shell 配置
    source ~/.bashrc 2>/dev/null || true
    
    if command -v q &> /dev/null; then
        Q_VERSION=$(q --version 2>/dev/null || echo "Unknown")
        echo "✅ 版本: $Q_VERSION"
    else
        echo "⚠️  請執行以下命令重新載入 PATH:"
        echo "   source ~/.bashrc"
        echo "   q --version"
    fi
    
    echo ""
    echo "🔐 下一步: 執行認證"
    echo "   q login"
    echo ""
    echo "🧪 測試連接:"
    echo "   q chat 'hello'"
    exit 0
fi

# 方法 3: 使用 wget
if command -v wget &> /dev/null; then
    echo "🔄 方法 3: 使用 wget 下載..."
    if wget -O ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null; then
        chmod +x ~/.local/bin/q
        
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        echo "✅ wget 安裝成功"
        source ~/.bashrc 2>/dev/null || true
        
        echo ""
        echo "🔐 下一步: 執行認證"
        echo "   q login"
        exit 0
    fi
fi

# 所有方法都失敗
echo "❌ 自動安裝失敗"
echo ""
echo "🔧 手動安裝選項:"
echo ""
echo "1. 檢查網路連接:"
echo "   ping -c 3 github.com"
echo ""
echo "2. 手動下載並安裝:"
echo "   wget https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
echo "   chmod +x q-linux-amd64"
echo "   sudo mv q-linux-amd64 /usr/local/bin/q"
echo ""
echo "3. 從 AWS 控制台下載:"
echo "   https://console.aws.amazon.com/"
echo "   搜尋 'Amazon Q Developer'"
echo ""
echo "4. 企業環境問題排解:"
echo "   - 檢查防火牆設定"
echo "   - 聯繫 IT 部門"
echo "   - 嘗試使用代理或 VPN"

exit 1