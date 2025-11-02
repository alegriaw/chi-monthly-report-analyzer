#!/bin/bash

# Amazon Q CLI Simple Installation Script
# One-liner installation based on AWS official blog

set -e

echo "🚀 Amazon Q CLI 簡易安裝"
echo "======================="

# Check if already installed
if command -v q &>/dev/null; then
    echo "✅ Amazon Q CLI 已安裝: $(q --version 2>/dev/null)"
    exit 0
fi

# Quick installation to user directory (no sudo required)
echo "📥 下載並安裝 Amazon Q CLI..."

# Create directory
mkdir -p ~/.local/bin

# Download and install
curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
chmod +x ~/.local/bin/q

# Add to PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ 安裝完成!"
echo ""
echo "📋 下一步:"
echo "1. source ~/.bashrc"
echo "2. q login"
echo "3. q chat 'hello'"