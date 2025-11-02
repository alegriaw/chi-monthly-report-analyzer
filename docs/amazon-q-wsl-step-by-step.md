# Amazon Q CLI WSL 逐步安裝指南

## 基於 AWS 官方 WSL 安裝方法

這個指南基於 AWS 官方文件，提供在 WSL 環境中安裝 Amazon Q CLI 的詳細步驟。

## 前置準備

確保你已經安裝並設定好 WSL (Windows Subsystem for Linux)，建議使用 Ubuntu 發行版。

## 安裝步驟

### 步驟 1: 進入 WSL 家目錄

```bash
cd
```

你會注意到目錄路徑已經改變。使用 `pwd` 命令確認你在正確的位置：

```bash
pwd
```

應該顯示 `/home/{你的用戶名}`，而不是 Windows 家目錄。

### 步驟 2: 安裝必要套件

首先我們需要安裝一些安裝程序需要的套件。使用 Ubuntu 的原生套件管理器：

```bash
sudo apt install unzip
```

系統會要求你輸入 Ubuntu 用戶的密碼（不是 Windows 密碼，除非你設定成一樣的！）。這會安裝 unzip 工具，應該不會花太長時間。

### 步驟 3: 下載安裝包

從 WSL 命令列使用以下命令下載包含安裝程序的 zip 檔案：

```bash
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" \
  -o "q.zip"
```

這會將安裝程序下載到你的當前目錄，也就是家目錄。

**重要檢查！** 確保你在 WSL 家目錄而不是 Windows 家目錄中執行。如果你使用 `pwd` 命令，它應該顯示 `/home/{你的用戶名}` - 如果不是，請再次執行 `cd` 命令。

### 步驟 4: 解壓縮安裝包

使用以下命令解壓縮：

```bash
unzip q.zip
```

這會創建一個名為 "q" 的子目錄，包含我們需要的所有檔案。

### 步驟 5: 準備安裝程序

我們幾乎準備好執行安裝程序了，但首先需要透過執行以下命令來啟用它：

```bash
cd q
chmod +x install.sh
```

`chmod` 命令會改變 Linux 中檔案的權限，我們正在啟用 install.sh 使其可執行，這樣我們就可以執行安裝程序。

### 步驟 6: 執行安裝程序

使用以下命令執行安裝程序：

```bash
./install.sh
```

系統會詢問你是否要修改你的 shell 配置。回答 **"Yes"**，因為這是在添加一個新的路徑來指向 Amazon Q Developer CLI 執行檔。

### 步驟 7: 啟用新的 Shell

安裝完成後，你需要啟用新的 shell。你可以退出並重新啟動你的 WSL 環境，或者只需輸入：

```bash
bash
```

## 登入 Amazon Q Developer

### 使用 Builder ID 登入

Amazon Q Developer 現在已安裝，下一階段是創建我們的 Builder ID 然後用它來登入。

從命令列輸入以下命令：

```bash
q login
```

你會看到兩個登入方法選項，可以使用上下箭頭鍵選擇。你要選擇第一個選項：**"Use for Free with Builder ID"**

當你選擇這個選項時，它會要求你在網頁瀏覽器中開啟一個 URL。複製這個 URL，然後在網頁瀏覽器中開啟它。

你現在需要創建一個新的 Builder ID，或者使用你可能已經擁有的現有 Builder ID 登入。

### 完成設定

登入完成後，你可以測試 Amazon Q CLI 是否正常工作：

```bash
q chat "hello"
```

如果一切正常，你應該會收到 Amazon Q 的回應。

## 驗證安裝

檢查安裝的版本：

```bash
q --version
```

檢查安裝位置：

```bash
which q
```

## 清理

安裝完成後，你可以清理下載的檔案：

```bash
cd ~
rm -f q.zip
rm -rf q
```

## 疑難排解

### 如果 `q` 命令找不到

1. 確保你已經重新啟動 bash：
   ```bash
   bash
   ```

2. 檢查 PATH 是否正確設定：
   ```bash
   echo $PATH
   ```

3. 手動重新載入 shell 配置：
   ```bash
   source ~/.bashrc
   ```

### 如果下載失敗

1. 檢查網路連接：
   ```bash
   ping google.com
   ```

2. 確保你在正確的目錄：
   ```bash
   pwd
   ```

3. 嘗試重新下載：
   ```bash
   rm -f q.zip
   curl --proto '=https' --tlsv1.2 -sSf \
     "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" \
     -o "q.zip"
   ```

## 下一步

安裝完成後，你可以：

1. **整合到 CHI Analyzer**: 啟動 CHI Low Security Score Analyzer，它會自動檢測 Amazon Q CLI
2. **探索功能**: 嘗試不同的 `q` 命令來熟悉功能
3. **查看幫助**: 使用 `q --help` 查看所有可用命令

這個安裝方法基於 AWS 官方指南，確保你獲得最穩定和最新的 Amazon Q CLI 版本。