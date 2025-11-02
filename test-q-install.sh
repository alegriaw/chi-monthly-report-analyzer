#!/bin/bash

# Quick test script for Amazon Q CLI installation
echo "🧪 Amazon Q CLI 安裝測試腳本"
echo "============================="

# Test GitHub download URL
echo ""
echo "🔗 測試 GitHub 下載 URL..."
if curl -I --connect-timeout 10 https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null | grep -q "200 OK"; then
    echo "✅ GitHub 下載 URL 可訪問"
else
    echo "❌ GitHub 下載 URL 無法訪問"
fi

# Test if we can download the file
echo ""
echo "📥 測試下載檔案..."
if curl -Lo /tmp/q-test https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64 2>/dev/null; then
    file_size=$(stat -c%s /tmp/q-test 2>/dev/null || echo "0")
    if [ "$file_size" -gt 1000000 ]; then  # Should be > 1MB
        echo "✅ 下載成功，檔案大小: $(($file_size / 1024 / 1024)) MB"
        
        # Check if it's a valid binary
        if file /tmp/q-test | grep -q "ELF.*executable"; then
            echo "✅ 檔案是有效的 Linux 執行檔"
        else
            echo "⚠️  檔案可能不是有效的執行檔"
        fi
        
        # Clean up
        rm -f /tmp/q-test
    else
        echo "❌ 下載的檔案太小，可能下載失敗"
    fi
else
    echo "❌ 下載失敗"
fi

# Check if q is already installed
echo ""
echo "🔍 檢查現有安裝..."
if command -v q &>/dev/null; then
    echo "✅ Amazon Q CLI 已安裝"
    echo "   路徑: $(which q)"
    echo "   版本: $(q --version 2>/dev/null || echo "無法獲取版本")"
else
    echo "⚠️  Amazon Q CLI 未安裝"
fi

echo ""
echo "📋 建議的安裝命令:"
echo ""
echo "方法 1 - 系統安裝 (需要 sudo):"
echo "curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
echo "chmod +x q && sudo mv q /usr/local/bin/"
echo ""
echo "方法 2 - 用戶安裝 (無需 sudo):"
echo "mkdir -p ~/.local/bin"
echo "curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64"
echo "chmod +x ~/.local/bin/q"
echo "echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "source ~/.bashrc"

echo ""
echo "測試完成！"