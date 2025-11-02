# Amazon Q CLI Installation Guide for Windows & WSL

## 概述

根據 [AWS 官方 blog](https://dev.to/aws/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows-lmh)，本指南提供在 Windows 和 WSL 環境中安裝 Amazon Q CLI 的完整步驟。

## Windows 環境安裝

### 方法 1: PowerShell 安裝 (Windows)

```powershell
# 在 PowerShell 中執行 (以管理員身份運行)
# 下載 Windows 版本
Invoke-WebRequest -Uri "https://github.com/aws/amazon-q-cli/releases/latest/download/q-windows-amd64.exe" -OutFile "q.exe"

# 移動到系統 PATH
Move-Item q.exe "C:\Windows\System32\q.exe"

# 驗證安裝
q --version
```

### 方法 2: 使用 Chocolatey (Windows)

```powershell
# 如果已安裝 Chocolatey
choco install amazon-q-cli
```

### 方法 3: 使用 Scoop (Windows)

```powershell
# 如果已安裝 Scoop
scoop install amazon-q-cli
```

## WSL 環境安裝

### 方法 1: 快速安裝腳本 (推薦)

```bash
# 使用我們提供的快速安裝腳本
bash quick-install-q.sh

# 或使用簡化版本
bash simple-install-q.sh
```

### 方法 2: 官方 WSL 安裝方法 (推薦)

基於 AWS 官方指南的 WSL 安裝步驟：

```bash
# 1. 確保在 WSL 家目錄
cd ~
pwd  # 應該顯示 /home/{username}

# 2. 安裝必要套件
sudo apt update
sudo apt install unzip curl

# 3. 下載官方安裝包
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" \
  -o "q.zip"

# 4. 解壓縮安裝包
unzip q.zip

# 5. 進入安裝目錄並設定權限
cd q
chmod +x install.sh

# 6. 執行安裝程序 (會詢問是否修改 shell 配置，請回答 Yes)
./install.sh

# 7. 重新載入 shell 配置
bash

# 8. 驗證安裝
q --version
```

### 方法 3: GitHub Releases 安裝

```bash
# 1. 創建安裝目錄
mkdir -p ~/.local/bin

# 2. 下載 Linux 版本 (適用於 WSL)
curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 3. 設定執行權限
chmod +x ~/.local/bin/q

# 4. 配置 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 5. 驗證安裝
q --version
```

### 方法 4: 系統安裝 (需要 sudo)

```bash
# 下載到臨時位置
curl -Lo /tmp/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 設定權限並移動到系統目錄
chmod +x /tmp/q
sudo mv /tmp/q /usr/local/bin/

# 驗證安裝
q --version
```

## 安裝後配置

### 1. 登入和認證

```bash
# 啟動登入流程
q login

# 選擇登入方法:
# 1. Use for Free with Builder ID (推薦)
# 2. Use with AWS IAM Identity Center

# 選擇 "Use for Free with Builder ID" 後會顯示 URL
# 複製 URL 到瀏覽器中完成 Builder ID 註冊或登入

# 驗證登入狀態
q chat "hello"
```

### 2. WSL 特定配置

#### 瀏覽器整合
在 WSL 中，`q login` 會嘗試開啟 Windows 預設瀏覽器：

```bash
# 如果瀏覽器無法自動開啟，會顯示 URL
# 手動複製 URL 到瀏覽器中完成認證
```

#### PATH 配置驗證
```bash
# 檢查 PATH 配置
echo $PATH | grep -o "$HOME/.local/bin"

# 如果沒有顯示結果，手動添加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## 版本管理和更新

### 檢查當前版本
```bash
q --version
```

### 更新到最新版本
```bash
# 重新運行安裝腳本
bash quick-install-q.sh

# 或手動更新
curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
chmod +x ~/.local/bin/q
```

### 卸載
```bash
# 移除二進位檔案
sudo rm -f /usr/local/bin/q
rm -f ~/.local/bin/q

# 清理 PATH 配置 (可選)
# 編輯 ~/.bashrc 移除 PATH 設定
```

## 疑難排解

### 常見問題

#### 1. "q: command not found"
```bash
# 檢查安裝位置
ls -la /usr/local/bin/q
ls -la ~/.local/bin/q

# 檢查 PATH
echo $PATH

# 重新載入 shell 配置
source ~/.bashrc
```

#### 2. "Permission denied"
```bash
# 檢查檔案權限
ls -la $(which q)

# 修正權限
chmod +x ~/.local/bin/q
# 或
sudo chmod +x /usr/local/bin/q
```

#### 3. 下載失敗
```bash
# 檢查網路連接
ping github.com

# 嘗試不同的下載方法
wget https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
```

#### 4. 登入問題
```bash
# 檢查認證狀態
q login --help

# 清除舊認證
rm -rf ~/.aws/sso/cache/

# 重新登入
q login
```

## 企業環境特殊配置

### 代理設定
```bash
# 設定 HTTP 代理
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# 重新嘗試安裝
bash quick-install-q.sh
```

### 防火牆配置
需要允許訪問以下域名：
- `github.com`
- `*.amazonaws.com`
- `*.aws.amazon.com`

## 整合到 CHI Analyzer

### 驗證整合
安裝完成後，在 CHI Analyzer 中：

1. **檢查狀態**: 側邊欄會顯示 Amazon Q CLI 狀態
2. **測試功能**: 嘗試生成 AI 摘要
3. **使用聊天**: 測試互動式聊天功能

### 日誌檢查
```bash
# 查看 CHI Analyzer 的 Amazon Q 日誌
tail -f amazon_q_cli.log
```

## 自動化腳本

### 快速安裝
```bash
# 完整功能的安裝腳本
bash quick-install-q.sh

# 簡化版本 (一鍵安裝)
bash simple-install-q.sh
```

### 網路診斷
```bash
# 如果遇到網路問題
bash diagnose-network.sh
```

### 完整部署
```bash
# 包含 Amazon Q CLI 檢測和安裝的完整部署
bash deploy-wsl.sh
```

## 參考資源

- **AWS 官方 Blog**: https://dev.to/aws/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows-lmh
- **GitHub Releases**: https://github.com/aws/amazon-q-cli/releases
- **AWS 官方文件**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/
- **CHI Analyzer 整合指南**: docs/amazon-q-integration.md

這個指南確保你能在 Windows 和 WSL 環境中成功安裝和配置 Amazon Q CLI，並與 CHI Low Security Score Analyzer 完美整合。