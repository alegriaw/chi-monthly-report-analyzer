#!/bin/bash

# Amazon Q CLI WSL Installation Script
# Based on AWS Official Installation Guide for WSL
# Optimized for WSL Ubuntu environments

set -e  # Exit on any error

echo "🚀 Amazon Q CLI WSL 安裝腳本"
echo "================================"
echo "📖 基於 AWS 官方 WSL 安裝指南"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if running in WSL
if [[ -f /proc/version ]] && grep -qi microsoft /proc/version; then
    print_status "檢測到 WSL 環境 - 使用官方 WSL 安裝方法"
elif [[ "$(uname)" == "Linux" ]]; then
    print_info "檢測到 Linux 環境 - 將使用 WSL 安裝方法"
else
    print_error "此腳本專為 WSL/Linux 環境設計"
    exit 1
fi

# Ensure we're in the home directory
echo ""
echo "📁 確保在 WSL 家目錄..."
cd ~
CURRENT_DIR=$(pwd)
print_info "當前目錄: $CURRENT_DIR"

if [[ "$CURRENT_DIR" != "/home/"* ]]; then
    print_warning "不在 WSL 家目錄，請確認環境"
    print_info "應該在 /home/{username} 目錄"
fi

# Check existing installation
echo ""
echo "🔍 檢查現有安裝..."
if command -v q &> /dev/null; then
    EXISTING_VERSION=$(q --version 2>/dev/null || echo "Unknown")
    EXISTING_PATH=$(which q)
    print_status "Amazon Q CLI 已安裝"
    echo "   路徑: $EXISTING_PATH"
    echo "   版本: $EXISTING_VERSION"
    echo ""
    
    read -p "是否要重新安裝最新版本? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "保持現有安裝，退出腳本"
        exit 0
    fi
    
    # Clean up existing installations
    print_info "清理現有安裝..."
    rm -rf ~/q 2>/dev/null || true
    rm -f ~/q.zip 2>/dev/null || true
fi

# Install required packages
echo ""
echo "📦 安裝必要套件..."
print_info "更新套件列表..."
sudo apt update

print_info "安裝 unzip 工具..."
if ! command -v unzip &> /dev/null; then
    sudo apt install -y unzip
    print_status "unzip 安裝完成"
else
    print_status "unzip 已安裝"
fi

# Install curl if not available
if ! command -v curl &> /dev/null; then
    print_info "安裝 curl..."
    sudo apt install -y curl
    print_status "curl 安裝完成"
else
    print_status "curl 已安裝"
fi

# Test network connectivity
echo ""
echo "🌐 測試網路連接..."
DOWNLOAD_URL="https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip"
if ! curl -I --connect-timeout 10 "$DOWNLOAD_URL" &>/dev/null; then
    print_error "無法連接到 Amazon Q 下載伺服器，請檢查網路連接"
    exit 1
fi
print_status "網路連接正常"

# Download Amazon Q CLI installer
echo ""
echo "📥 下載 Amazon Q CLI 安裝包..."
print_info "從: $DOWNLOAD_URL"

# Clean up any existing files
rm -f ~/q.zip 2>/dev/null || true
rm -rf ~/q 2>/dev/null || true

if curl --proto '=https' --tlsv1.2 -sSf "$DOWNLOAD_URL" -o "q.zip"; then
    print_status "下載完成: q.zip"
    
    # Verify download
    FILE_SIZE=$(stat -c%s "q.zip" 2>/dev/null || echo "0")
    if [[ $FILE_SIZE -lt 100000 ]]; then  # Should be > 100KB
        print_error "下載的檔案太小 ($FILE_SIZE bytes)，可能下載失敗"
        rm -f "q.zip"
        exit 1
    fi
    
    print_status "檔案驗證通過 (${FILE_SIZE} bytes)"
else
    print_error "下載失敗"
    exit 1
fi

# Extract the installer
echo ""
echo "📦 解壓縮安裝包..."
if unzip q.zip; then
    print_status "解壓縮完成"
    
    # Verify extraction
    if [[ ! -d "q" ]]; then
        print_error "解壓縮後找不到 q 目錄"
        exit 1
    fi
    
    if [[ ! -f "q/install.sh" ]]; then
        print_error "找不到安裝腳本 q/install.sh"
        exit 1
    fi
    
    print_status "安裝檔案準備完成"
else
    print_error "解壓縮失敗"
    exit 1
fi

# Prepare and run installer
echo ""
echo "🔧 準備安裝程序..."
cd q

print_info "設定執行權限..."
chmod +x install.sh
print_status "權限設定完成"

# Run the installer
echo ""
echo "🚀 執行 Amazon Q CLI 安裝程序..."
print_warning "安裝程序會詢問是否修改 shell 配置，請回答 'Yes'"
echo ""

if ./install.sh; then
    print_status "Amazon Q CLI 安裝程序執行完成"
else
    print_error "安裝程序執行失敗"
    exit 1
fi

# Return to home directory and clean up
cd ~
rm -f q.zip
rm -rf q

# Reload shell configuration
echo ""
echo "🔄 重新載入 shell 配置..."
if [[ -f ~/.bashrc ]]; then
    source ~/.bashrc 2>/dev/null || true
    print_status "已重新載入 ~/.bashrc"
fi

# Alternative: start new bash session
print_info "啟動新的 bash 會話以確保 PATH 更新..."
exec bash -c "
    echo '✅ 新 bash 會話已啟動'
    
    # Continue with verification in new session
    if command -v q &>/dev/null; then
        echo '✅ Amazon Q CLI 安裝成功!'
        echo \"   路徑: \$(which q)\"
        echo \"   版本: \$(q --version 2>/dev/null || echo 'Unknown')\"
    else
        echo '❌ 安裝驗證失敗，q 命令不可用'
        echo '請嘗試手動執行: bash'
        exit 1
    fi
    
    echo ''
    echo '📋 下一步操作:'
    echo '1. 登入 Amazon Q (選擇 \"Use for Free with Builder ID\"):'
    echo '   q login'
    echo ''
    echo '2. 測試連接:'
    echo '   q chat \"hello\"'
    echo ''
    
    # Ask if user wants to login now
    read -p '是否現在就登入 Amazon Q? (y/N): ' -n 1 -r
    echo
    if [[ \$REPLY =~ ^[Yy]$ ]]; then
        echo '🔐 啟動 Amazon Q 登入流程...'
        echo '請選擇 \"Use for Free with Builder ID\" 選項'
        q login
    fi
    
    echo ''
    echo '🎉 Amazon Q CLI WSL 安裝完成!'
"

# Note: Verification and next steps are handled in the new bash session above