# Amazon Q CLI Installation Guide for WSL

## 概述

本指南說明如何在 WSL (Windows Subsystem for Linux) 環境中正確安裝和配置 Amazon Q CLI。

## 安裝方法

根據 [AWS 官方文件](https://docs.aws.amazon.com/zh_tw/amazonq/latest/qdeveloper-ug/command-line-installing.html)，以下是在 WSL/Linux 中安裝 Amazon Q CLI 的正確方法：

### 方法 1: 從 GitHub Releases 下載 (推薦)

根據 [AWS 官方 blog](https://dev.to/aws/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows-lmh)，最可靠的安裝方法是直接從 GitHub 下載：

```bash
# 下載最新版本的 Amazon Q CLI
curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 設定執行權限
chmod +x q

# 移動到系統 PATH (需要 sudo)
sudo mv q /usr/local/bin/

# 驗證安裝
q --version
```

### 方法 2: 使用 wget 下載

```bash
# 使用 wget 下載
wget https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 設定執行權限
chmod +x q-linux-amd64

# 移動到系統 PATH (需要 sudo 權限)
sudo mv q-linux-amd64 /usr/local/bin/q

# 驗證安裝
q --version
```

### 方法 3: 安裝到用戶目錄 (無需 sudo，推薦)

這是最安全的安裝方法，不需要管理員權限：

```bash
# 1. 創建用戶 bin 目錄
mkdir -p ~/.local/bin

# 2. 下載到用戶目錄
curl -Lo ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 3. 設定執行權限
chmod +x ~/.local/bin/q

# 4. 添加到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 5. 重新載入配置
source ~/.bashrc

# 6. 驗證安裝
q --version
```

### 方法 4: 網路問題排解和替代方案

如果遇到 `Could not resolve host` 錯誤，請嘗試以下方法：

#### 4.1 檢查網路連接
```bash
# 測試基本網路連接
ping amazon.com

# 測試 DNS 解析
nslookup d2yblsmsllhwuq.cloudfront.net

# 測試 HTTPS 連接
curl -I https://amazon.com
```

#### 4.2 使用 GitHub Releases (最可靠)
```bash
# 直接從 GitHub 下載 (最可靠的方法)
curl -Lo q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64

# 或使用 wget
wget https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
```

#### 4.3 使用 AWS CLI (如果已安裝)
```bash
# 通過 AWS CLI 下載
aws s3 cp s3://amazon-q-cli/latest/q-linux-amd64 ~/.local/bin/q
chmod +x ~/.local/bin/q
```

#### 4.4 企業環境解決方案
```bash
# 設定代理 (如果需要)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# 然後重試安裝
curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh
```

#### 4.5 手動下載 (最可靠)
1. **從 AWS 控制台下載**：
   - 登入 AWS 控制台
   - 搜尋 "Amazon Q"
   - 下載 CLI 工具

2. **從 GitHub 下載** (如果可用)：
   - 訪問 GitHub releases 頁面
   - 下載適合的版本

3. **安裝下載的檔案**：
   ```bash
   chmod +x q-linux-amd64
   sudo mv q-linux-amd64 /usr/local/bin/q
   ```

## 配置和認證

### 1. 登入 Amazon Q

```bash
# 啟動登入流程 (會開啟瀏覽器)
q login

# 或使用特定的認證方式
q auth login
```

### 2. 驗證認證狀態

```bash
# 檢查認證狀態
q auth status

# 測試連接
q chat "hello"
```

### 3. 登出 (如需要)

```bash
q logout
# 或
q auth logout
```

## 常見問題排解

### 問題 1: 找不到 `q` 命令

**症狀**: `q: command not found`

**解決方案**:
```bash
# 檢查 q 是否存在
ls -la ~/.local/bin/q

# 檢查 PATH
echo $PATH

# 手動添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 永久添加到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 問題 2: 權限錯誤

**症狀**: `Permission denied`

**解決方案**:
```bash
# 設定正確的執行權限
chmod +x ~/.local/bin/q

# 檢查檔案權限
ls -la ~/.local/bin/q
```

### 問題 3: 認證失敗

**症狀**: `not logged in` 或認證錯誤

**解決方案**:
```bash
# 清除舊的認證
q logout

# 重新登入
q login

# 檢查 AWS 認證配置
aws configure list
```

### 問題 4: 網路連接問題

**症狀**: `Could not resolve host` 或連接超時

**診斷步驟**:
```bash
# 1. 檢查基本網路連接
ping -c 3 amazon.com

# 2. 檢查 DNS 解析
nslookup d2yblsmsllhwuq.cloudfront.net
dig d2yblsmsllhwuq.cloudfront.net

# 3. 檢查防火牆和代理
echo "HTTP_PROXY: $HTTP_PROXY"
echo "HTTPS_PROXY: $HTTPS_PROXY"

# 4. 測試 HTTPS 連接
curl -I https://d2yblsmsllhwuq.cloudfront.net

# 5. 測試 AWS 服務連接
curl -I https://s3.amazonaws.com
```

**解決方案**:

1. **DNS 問題**:
   ```bash
   # 嘗試使用不同的 DNS
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf.backup
   echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf.backup
   sudo cp /etc/resolv.conf.backup /etc/resolv.conf
   ```

2. **代理設定**:
   ```bash
   # 設定代理 (替換為你的代理地址)
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   export NO_PROXY=localhost,127.0.0.1
   ```

3. **企業防火牆**:
   - 聯繫 IT 部門請求允許訪問：
     - `*.cloudfront.net`
     - `*.amazonaws.com`
     - `github.com` (如果使用 GitHub 下載)

4. **使用備用方法**:
   ```bash
   # 方法 A: 使用 AWS CLI
   aws s3 cp s3://amazon-q-cli/latest/q-linux-amd64 ./q
   
   # 方法 B: 手動從 AWS 控制台下載
   # 登入 AWS 控制台 → Amazon Q → 下載 CLI
   ```

## WSL 特定注意事項

### 1. 路徑配置

在 WSL 中，確保使用 Linux 路徑格式：
```bash
# 正確 ✅
~/.local/bin/q

# 錯誤 ❌
C:\Users\username\.local\bin\q
```

### 2. 瀏覽器整合

Amazon Q CLI 登入會嘗試開啟瀏覽器：
- WSL 會自動開啟 Windows 預設瀏覽器
- 如果無法自動開啟，會顯示 URL 供手動複製

### 3. 檔案權限

WSL 中的檔案權限可能需要特別注意：
```bash
# 檢查並修正權限
chmod 755 ~/.local/bin/q
```

## 整合到 CHI Analyzer

### 1. 驗證整合

在 CHI Analyzer 中，Amazon Q CLI 狀態會顯示在側邊欄：
- ✅ 綠色：已安裝且已認證
- ⚠️ 黃色：已安裝但未認證
- ❌ 紅色：未安裝

### 2. 功能測試

```bash
# 在 CHI Analyzer 外測試
q chat "Generate a summary of security improvements"

# 檢查日誌
tail -f amazon_q_cli.log
```

### 3. 疑難排解

如果 CHI Analyzer 中的 Amazon Q 功能不工作：

1. **檢查 CLI 狀態**
   ```bash
   q --version
   q auth status
   ```

2. **測試基本功能**
   ```bash
   q chat "hello"
   ```

3. **檢查應用程式日誌**
   ```bash
   tail -f amazon_q_cli.log
   ```

4. **重新啟動應用程式**
   ```bash
   # 停止 Streamlit
   pkill -f streamlit
   
   # 重新啟動
   ./deploy-wsl.sh
   ```

## 版本管理

### 檢查版本

```bash
q --version
```

### 更新 Amazon Q CLI

```bash
# 方法 1: 重新安裝
curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh

# 方法 2: 手動下載新版本
wget -O ~/.local/bin/q https://github.com/aws/amazon-q-cli/releases/latest/download/q-linux-amd64
chmod +x ~/.local/bin/q
```

## 安全考量

### 1. 認證資訊

- Amazon Q CLI 認證資訊儲存在 `~/.aws/` 目錄
- 不要分享或提交認證檔案到版本控制

### 2. 權限管理

- 確保 Amazon Q CLI 二進位檔案只有適當的執行權限
- 定期檢查和更新 AWS IAM 權限

### 3. 網路安全

- 在企業環境中，可能需要配置代理或防火牆規則
- 確保 HTTPS 連接到 AWS 服務

## 支援和資源

- **AWS 官方文件**: https://docs.aws.amazon.com/amazonq/
- **GitHub Issues**: https://github.com/aws/amazon-q-cli/issues
- **AWS 支援**: 透過 AWS 控制台提交支援案例

## 自動化腳本

CHI Analyzer 提供了自動化的安裝和檢測腳本：

```bash
# 使用 deploy-wsl.sh 自動檢測和安裝
./deploy-wsl.sh
```

這個腳本會：
1. 檢測 Amazon Q CLI 是否已安裝
2. 驗證認證狀態
3. 提供安裝選項（如果未安裝）
4. 啟動 CHI Analyzer 應用程式