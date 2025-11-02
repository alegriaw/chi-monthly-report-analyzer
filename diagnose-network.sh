#!/bin/bash

# Amazon Q CLI Network Diagnostics Script
# This script helps diagnose network connectivity issues

echo "🔍 Amazon Q CLI 網路診斷工具"
echo "================================"

# Check basic network connectivity
echo ""
echo "📡 檢查基本網路連接..."
if ping -c 3 amazon.com &>/dev/null; then
    echo "✅ 基本網路連接正常"
else
    echo "❌ 基本網路連接失敗"
    echo "💡 請檢查網路連接或聯繫網路管理員"
fi

# Check DNS resolution
echo ""
echo "🌐 檢查 DNS 解析..."
if nslookup d2yblsmsllhwuq.cloudfront.net &>/dev/null; then
    echo "✅ DNS 解析正常"
    echo "   解析結果:"
    nslookup d2yblsmsllhwuq.cloudfront.net | grep -A 2 "Name:"
else
    echo "❌ DNS 解析失敗"
    echo "💡 嘗試解決方案:"
    echo "   1. 更換 DNS 伺服器: echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf"
    echo "   2. 清除 DNS 快取: sudo systemctl restart systemd-resolved"
fi

# Check proxy settings
echo ""
echo "🔒 檢查代理設定..."
if [ -n "$HTTP_PROXY" ] || [ -n "$HTTPS_PROXY" ]; then
    echo "⚠️  檢測到代理設定:"
    echo "   HTTP_PROXY: ${HTTP_PROXY:-未設定}"
    echo "   HTTPS_PROXY: ${HTTPS_PROXY:-未設定}"
    echo "   NO_PROXY: ${NO_PROXY:-未設定}"
else
    echo "✅ 未使用代理"
fi

# Test HTTPS connectivity to Amazon Q CLI CDN
echo ""
echo "🔗 測試 Amazon Q CLI CDN 連接..."
if curl -I --connect-timeout 10 https://d2yblsmsllhwuq.cloudfront.net &>/dev/null; then
    echo "✅ Amazon Q CLI CDN 連接正常"
else
    echo "❌ Amazon Q CLI CDN 連接失敗"
    echo "💡 可能的原因:"
    echo "   1. 企業防火牆阻擋"
    echo "   2. 地理位置限制"
    echo "   3. CDN 暫時不可用"
fi

# Test alternative URLs
echo ""
echo "🔄 測試備用下載源..."

# Test AWS S3
if curl -I --connect-timeout 10 https://s3.amazonaws.com &>/dev/null; then
    echo "✅ AWS S3 連接正常"
else
    echo "❌ AWS S3 連接失敗"
fi

# Test GitHub (alternative source)
if curl -I --connect-timeout 10 https://github.com &>/dev/null; then
    echo "✅ GitHub 連接正常"
else
    echo "❌ GitHub 連接失敗"
fi

# Check if AWS CLI is available
echo ""
echo "🛠️  檢查 AWS CLI 可用性..."
if command -v aws &>/dev/null; then
    echo "✅ AWS CLI 已安裝"
    echo "   版本: $(aws --version 2>&1 | head -n1)"
    
    # Test AWS CLI connectivity
    if aws sts get-caller-identity &>/dev/null; then
        echo "✅ AWS CLI 認證正常"
        echo "💡 可以使用 AWS CLI 下載 Amazon Q CLI:"
        echo "   aws s3 cp s3://amazon-q-cli/latest/q-linux-amd64 ~/.local/bin/q"
    else
        echo "⚠️  AWS CLI 未認證"
    fi
else
    echo "⚠️  AWS CLI 未安裝"
fi

# Provide recommendations
echo ""
echo "📋 建議的解決方案:"
echo ""

if ping -c 1 amazon.com &>/dev/null; then
    if ! nslookup d2yblsmsllhwuq.cloudfront.net &>/dev/null; then
        echo "🔧 DNS 問題解決方案:"
        echo "   sudo echo 'nameserver 8.8.8.8' > /etc/resolv.conf"
        echo "   sudo echo 'nameserver 1.1.1.1' >> /etc/resolv.conf"
    elif ! curl -I --connect-timeout 10 https://d2yblsmsllhwuq.cloudfront.net &>/dev/null; then
        echo "🔧 防火牆/代理問題解決方案:"
        echo "   1. 聯繫 IT 部門請求允許訪問 *.cloudfront.net"
        echo "   2. 設定代理 (如果需要):"
        echo "      export HTTP_PROXY=http://proxy:port"
        echo "      export HTTPS_PROXY=http://proxy:port"
        echo "   3. 使用備用安裝方法 (見下方)"
    fi
else
    echo "🔧 網路連接問題解決方案:"
    echo "   1. 檢查網路線或 WiFi 連接"
    echo "   2. 重啟網路服務: sudo systemctl restart networking"
    echo "   3. 聯繫網路管理員"
fi

echo ""
echo "🛠️  備用安裝方法:"
echo "   1. 手動從 AWS 控制台下載"
echo "   2. 使用 AWS CLI (如果可用)"
echo "   3. 從同事或其他來源獲取二進位檔案"
echo "   4. 使用企業內部軟體倉庫"

echo ""
echo "📞 需要幫助？"
echo "   - 查看詳細安裝指南: docs/amazon-q-cli-installation.md"
echo "   - 聯繫 IT 支援部門"
echo "   - 參考 AWS 官方文件"

echo ""
echo "診斷完成！"