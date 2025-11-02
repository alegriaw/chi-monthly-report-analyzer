# GitHub 設置說明

## 問題
Git 推送失敗，因為需要身份驗證。GitHub 不再支持密碼驗證，需要使用以下方法之一：

## 解決方案

### 方法 1: 使用設置腳本 (推薦)
```bash
./setup-git.sh
```

### 方法 2: 手動設置 Personal Access Token

1. **創建 Personal Access Token**:
   - 訪問 https://github.com/settings/tokens
   - 點擊 "Generate new token (classic)"
   - 名稱: `CHI Analyzer`
   - 權限: 選擇 `repo` (完整倉庫權限)
   - 點擊 "Generate token"
   - **複製 token** (只會顯示一次!)

2. **配置 Git**:
   ```bash
   git remote set-url origin https://alegriaw:YOUR_TOKEN@github.com/alegriaw/chi-monthly-report-analyzer.git
   git push -u origin main
   ```

### 方法 3: 使用 SSH Key

1. **添加 SSH Key 到 GitHub**:
   - 複製這個公鑰:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEUZWZk5UK3Ub2IskGyRG3aqIYa1Q0kjNEHTghuP09E8 alegriaw@users.noreply.github.com
   ```
   - 訪問 https://github.com/settings/ssh
   - 點擊 "New SSH key"
   - 貼上公鑰並保存

2. **配置 Git**:
   ```bash
   git remote set-url origin git@github.com:alegriaw/chi-monthly-report-analyzer.git
   git push -u origin main
   ```

## 驗證設置

推送成功後，你可以在以下位置查看倉庫:
https://github.com/alegriaw/chi-monthly-report-analyzer

## 安全提醒

- Personal Access Token 要妥善保管
- 不要在公開場所分享 token
- 定期更新 token (建議設置過期時間)