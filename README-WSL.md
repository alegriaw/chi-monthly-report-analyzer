# CHI Low Security Score Analyzer - WSL Deployment Guide

## 概述

本指南說明如何在 Windows Subsystem for Linux (WSL) 環境中部署和運行 CHI Low Security Score Analyzer，確保應用程式始終在 WSL 環境中運行以獲得最佳性能和兼容性。

## 為什麼使用 WSL？

- **Amazon Q CLI 兼容性**: Amazon Q CLI 在 Linux 環境中運行更穩定
- **Python 環境**: 更好的 Python 套件兼容性和性能
- **開發工具**: 完整的 Linux 開發環境
- **網路配置**: 更好的網路服務配置選項

## 快速開始

### 方法 1: 從 Windows 啟動（推薦）

1. **雙擊執行** `start-wsl.bat`
2. **等待啟動** - 腳本會自動在 WSL 中啟動應用程式
3. **開啟瀏覽器** 前往 `http://localhost:8501`

### 方法 2: 在 WSL 中直接啟動


1. **開啟 WSL 終端機**
2. **進入專案目錄**:
   ```bash
   cd ~/Dev/Project/DevTAM/chi-monthly-report
   ```
3. **執行部署腳本**:
   ```bash
   ./deploy-wsl.sh
   ```

## 安裝和配置

### 初次設置

1. **確保 WSL 已安裝**:
   ```cmd
   wsl --install
   ```

2. **安裝應用程式依賴**:
   ```bash
   ./install.sh
   ```

3. **配置 WSL 環境**:
   ```bash
   ./wsl-config.sh
   ```

4. **重新載入配置**:
   ```bash
   source ~/.bashrc
   ```

### 驗證安裝

執行以下命令檢查安裝狀態：
```bash
./deploy-wsl.sh
```

應該看到：
- ✅ Running in WSL environment
- ✅ Virtual environment found
- ✅ All dependencies installed
- 🚀 Application starting...

## 功能特色

### 自動環境檢測
- 確保在 WSL 環境中運行
- 自動檢查和安裝依賴項
- 驗證 Amazon Q CLI 狀態

### 網路配置
- 自動配置適合 WSL 的網路設定
- 支援本地和網路訪問
- 顯示所有可用的 URL

### 進程管理
- 自動停止現有的 Streamlit 進程
- 防止端口衝突
- 優雅的應用程式重啟

### 系統整合
- 創建桌面快捷方式
- 設置系統別名
- 可選的 systemd 服務配置

## 使用方式

### 基本操作

1. **啟動應用程式**:
   ```bash
   chi-analyzer
   ```
   或
   ```bash
   ./deploy-wsl.sh
   ```

2. **停止應用程式**:
   按 `Ctrl+C`

3. **檢查狀態**:
   ```bash
   ps aux | grep streamlit
   ```

### 高級操作

#### 作為系統服務運行

1. **啟用服務**:
   ```bash
   systemctl --user enable chi-analyzer
   ```

2. **啟動服務**:
   ```bash
   systemctl --user start chi-analyzer
   ```

3. **檢查服務狀態**:
   ```bash
   systemctl --user status chi-analyzer
   ```

#### 自定義配置

編輯 `~/.config/chi-analyzer/wsl-env.conf`:
```bash
export CHI_ANALYZER_PORT=8502  # 更改端口
export CHI_ANALYZER_HOST=127.0.0.1  # 限制本地訪問
```

## 網路訪問

應用程式啟動後，可以通過以下 URL 訪問：

- **本地訪問**: `http://localhost:8501`
- **WSL IP 訪問**: `http://[WSL_IP]:8501`
- **網路訪問**: `http://[HOSTNAME]:8501`

## Amazon Q CLI 整合

### 詳細安裝指南

**📖 完整的 Amazon Q CLI 安裝和配置指南：[docs/amazon-q-cli-installation.md](docs/amazon-q-cli-installation.md)**

新增的詳細安裝指南涵蓋：

#### 🔧 安裝方法
- **官方安裝腳本**: 一鍵自動安裝和配置
- **手動下載安裝**: 適用於受限環境
- **用戶目錄安裝**: 無需 sudo 權限的安裝方式
- **網路問題排解**: 代理、DNS、企業環境解決方案

#### 🖥️ WSL 特定功能
- **路徑配置**: Linux 路徑格式和環境變數設定
- **瀏覽器整合**: WSL 與 Windows 瀏覽器的認證流程
- **檔案權限**: WSL 環境中的正確權限設定
- **系統整合**: 與 CHI Analyzer 的無縫整合

#### 🛠️ 疑難排解
- **常見錯誤解決**: 詳細的錯誤診斷和解決步驟
- **網路連接問題**: 企業代理和防火牆配置
- **認證管理**: 登入/登出流程和狀態檢查
- **版本兼容性**: 不同版本的 CLI 命令格式

#### 🔒 安全和最佳實務
- **認證資訊管理**: 安全的憑證儲存和管理
- **權限設定**: 最小權限原則和 IAM 配置
- **網路安全**: HTTPS 連接和企業安全要求

### 快速安裝

```bash
# 自動安裝（推薦）
curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh
source ~/.bashrc

# 登入 Amazon Q
q login

# 驗證狀態
q chat "hello"
```

## 疑難排解

### 常見問題

#### 1. WSL 未安裝或無法訪問
```cmd
# 在 Windows PowerShell 中執行
wsl --install
wsl --update
```

#### 2. 虛擬環境問題
```bash
# 重新創建虛擬環境
rm -rf chi_analyzer_env
python3 -m venv chi_analyzer_env
source chi_analyzer_env/bin/activate
pip install -r requirements.txt
```

#### 3. 端口被占用
```bash
# 查找占用端口的進程
sudo netstat -tlnp | grep :8501

# 停止進程
sudo kill -9 [PID]
```

#### 4. Amazon Q CLI 問題

**📖 完整的 Amazon Q CLI 安裝和疑難排解指南：[docs/amazon-q-cli-installation.md](docs/amazon-q-cli-installation.md)**

該指南包含：
- **多種安裝方法**: 自動腳本、手動下載、用戶目錄安裝
- **WSL 特定配置**: 路徑設定、瀏覽器整合、權限管理
- **網路問題解決**: 代理設定、DNS 解析、企業環境配置
- **詳細疑難排解**: 常見錯誤和解決方案
- **與 CHI Analyzer 整合**: 應用程式特定的配置和測試

```bash
# 快速重新安裝
curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh

# 重新登入
q logout
q login

# 檢查詳細狀態
q --version
q auth status
```

### 日誌檢查

- **應用程式日誌**: `amazon_q_cli.log`
- **系統日誌**: `journalctl --user -u chi-analyzer`
- **Streamlit 日誌**: 在終端機中直接顯示

### 性能優化

1. **增加 WSL 記憶體限制**:
   編輯 `%USERPROFILE%\.wslconfig`:
   ```ini
   [wsl2]
   memory=4GB
   processors=2
   ```

2. **優化 Python 性能**:
   ```bash
   export PYTHONUNBUFFERED=1
   export PYTHONDONTWRITEBYTECODE=1
   ```

## 檔案結構

```
chi-monthly-report/
├── deploy-wsl.sh              # WSL 部署腳本
├── start-wsl.bat              # Windows 啟動器
├── wsl-config.sh              # WSL 配置腳本
├── README-WSL.md              # WSL 部署指南
├── chi_analyzer_env/          # Python 虛擬環境
├── chi_low_security_score_analyzer.py  # 主應用程式
└── requirements.txt           # Python 依賴項
```

## 最佳實務

1. **始終在 WSL 中運行**: 使用提供的腳本確保環境一致性
2. **定期更新**: 保持 WSL、Python 和依賴項的最新版本
3. **備份配置**: 定期備份 `~/.config/chi-analyzer/` 目錄
4. **監控資源**: 注意 WSL 的記憶體和 CPU 使用情況
5. **日誌管理**: 定期清理舊的日誌檔案

## 支援

如果遇到問題：

1. **檢查日誌**: 查看應用程式和系統日誌
2. **驗證環境**: 確保所有依賴項正確安裝
3. **重新配置**: 執行 `./wsl-config.sh` 重新配置環境
4. **重新安裝**: 如有必要，重新執行完整安裝流程

---

**注意**: 本指南假設使用 Ubuntu WSL 發行版。其他發行版可能需要調整部分命令。