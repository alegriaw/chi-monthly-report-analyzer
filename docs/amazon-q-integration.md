# Amazon Q CLI Integration Guide

## 概述

CHI Low Security Score Analyzer 整合了 Amazon Q CLI，提供 AI 驅動的分析摘要功能。本文件說明如何在程式中執行 Q CLI 登入和管理功能。

## 功能特色

### 1. 增強的認證管理
- **智能登入檢測**: 自動檢測多種 CLI 命令格式和版本差異
- **多層次狀態檢查**: 使用三種方法確保準確的認證狀態檢測
  - 快速登入狀態檢查（5秒超時）
  - 幫助命令驗證（3秒超時）
  - 簡單聊天測試（8秒超時）
- **優化的性能**: 避免使用慢速聊天命令進行狀態檢查
- **優雅的錯誤處理**: 提供詳細的錯誤訊息和解決建議
- **手動登入備案**: 當自動登入失敗時提供清晰的手動操作指引
- **即時狀態更新**: 實時顯示認證狀態和連線品質

### 2. 專業 AI 摘要生成
- **上下文感知分析**: 基於實際客戶數據生成專業月度報告
- **自動檔案儲存**: 生成的摘要自動儲存為帶時間戳的 markdown 檔案
- **格式化輸出**: 清理 ANSI 代碼，提供乾淨的 markdown 格式
- **錯誤恢復**: 智能處理 API 限制和網路問題

### 3. 互動式聊天界面
- **多輪對話**: 支援連續對話，保持上下文連貫性
- **聊天歷史**: 完整的對話記錄和管理功能
- **快速問題**: 預定義的常見分析問題，一鍵提問
- **摘要改進**: 通過對話優化和自定義生成的摘要

### 4. 增強的使用者體驗
- **視覺化狀態指示**: 清晰的圖標和顏色編碼狀態顯示
- **詳細的故障排除**: 內建的診斷和解決方案建議
- **命令檢測**: 自動適應不同版本的 Amazon Q CLI 命令格式
- **優雅降級**: 當 AI 功能不可用時提供替代方案

## 程式中的實作

### 增強的認證檢測機制

新版本的認證檢測採用多層次方法，大幅提升了檢測速度和準確性：

#### 檢測流程
1. **版本檢查**: 首先確認 Amazon Q CLI 已安裝
2. **快速登入檢查**: 使用 `q login` 命令檢查是否已認證（5秒超時）
3. **幫助命令驗證**: 如果登入檢查不明確，測試 `q chat --help`（3秒超時）
4. **簡單聊天測試**: 最後使用簡短的聊天命令進行最終驗證（8秒超時）

#### 性能優化
- **避免慢速命令**: 不再使用完整的聊天命令作為主要檢測方法
- **階段式超時**: 每個檢測階段使用適當的超時設定
- **智能降級**: 即使某些測試失敗，仍能提供有用的狀態資訊
- **錯誤容忍**: 網路問題或超時不會導致完全失敗
- **狀態緩存**: 5分鐘緩存機制避免頻繁檢查 (詳見 [Cache Duration Analysis](cache-duration-analysis.md))

#### 狀態回報改進
- **詳細狀態訊息**: 提供具體的檢測結果和建議
- **部分可用性**: 即使聊天功能有問題，仍能識別 CLI 可用性
- **超時處理**: 優雅處理網路延遲和連線問題

### 核心函數

#### 1. `amazon_q_login()` - 自動登入
```python
def amazon_q_login() -> tuple[bool, str]:
    """Attempt to login to Amazon Q CLI programmatically"""
    try:
        # 檢查 CLI 是否已安裝
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            return False, "Amazon Q CLI not installed. Please install it first."
        
        # 執行登入命令 - 會開啟瀏覽器進行認證
        login_result = subprocess.run(['q', 'auth', 'login'], 
                                    capture_output=True, text=True, timeout=60)
        
        if login_result.returncode == 0:
            return True, "Login successful! Amazon Q is now available."
        else:
            error_msg = login_result.stderr.strip() or login_result.stdout.strip()
            return False, f"Login failed: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return False, "Login timed out. Please try again or login manually in terminal."
    except Exception as e:
        return False, f"Login error: {str(e)}"
```

#### 2. `amazon_q_logout()` - 登出
```python
def amazon_q_logout() -> tuple[bool, str]:
    """Logout from Amazon Q CLI"""
    try:
        logout_result = subprocess.run(['q', 'auth', 'logout'], 
                                     capture_output=True, text=True, timeout=30)
        
        if logout_result.returncode == 0:
            return True, "Logout successful!"
        else:
            error_msg = logout_result.stderr.strip() or logout_result.stdout.strip()
            return False, f"Logout failed: {error_msg}"
            
    except Exception as e:
        return False, f"Logout error: {str(e)}"
```

#### 3. `check_amazon_q_availability()` - 增強的狀態檢測
```python
def check_amazon_q_availability() -> tuple[bool, str]:
    """Enhanced Amazon Q CLI availability check with optimized authentication detection"""
    try:
        # 檢查 CLI 是否已安裝
        version_result = subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode != 0:
            return False, "Amazon Q CLI not installed"
        
        # 使用更快速的登入狀態檢查，而非聊天命令
        try:
            # 方法 1: 嘗試登入命令檢查是否已登入（最快速）
            login_check = subprocess.run(['q', 'login'], capture_output=True, text=True, timeout=5)
            stderr_lower = login_check.stderr.lower()
            stdout_lower = login_check.stdout.lower()
            
            if ("already logged in" in stderr_lower or "already logged in" in stdout_lower or
                "you are already authenticated" in stderr_lower or "you are already authenticated" in stdout_lower):
                return True, "Available and authenticated"
            
            # 方法 2: 如果登入檢查未顯示「已登入」，嘗試幫助命令
            help_result = subprocess.run(['q', 'chat', '--help'], capture_output=True, text=True, timeout=3)
            if help_result.returncode == 0:
                # 如果幫助命令有效，可能已登入，進行快速測試
                try:
                    test_result = subprocess.run(['q', 'chat', 'hi'], capture_output=True, text=True, timeout=8)
                    if test_result.returncode == 0:
                        return True, "Available and authenticated"
                    elif "not logged in" in test_result.stderr.lower():
                        return False, "Not logged in"
                    else:
                        # 聊天失敗但可能仍已登入
                        return True, "Available (chat test failed but CLI detected)"
                except subprocess.TimeoutExpired:
                    return True, "Available (chat test timed out but CLI detected)"
            else:
                # 幫助命令失敗，可能未登入
                if "not logged in" in help_result.stderr.lower():
                    return False, "Not logged in"
                else:
                    return False, f"CLI error: {help_result.stderr[:100]}"
                    
        except subprocess.TimeoutExpired:
            return True, "Available (status check timed out but CLI detected)"
            
    except subprocess.TimeoutExpired:
        return False, "Status check timed out"
    except FileNotFoundError:
        return False, "Amazon Q CLI not found"
    except Exception as e:
        return False, f"Error checking Amazon Q: {str(e)}"
```

#### 4. `chat_with_amazon_q()` - 互動式聊天
```python
def chat_with_amazon_q(message: str, context: str = "") -> tuple[bool, str]:
    """Interactive chat with Amazon Q CLI"""
    try:
        logger.info(f"Sending chat message to Amazon Q: {message[:100]}...")
        
        # 結合上下文和訊息
        full_prompt = f"{context}\n\nUser Question: {message}" if context else message
        
        # 呼叫 Amazon Q CLI
        result = subprocess.run([
            'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
        ], capture_output=True, text=True, timeout=45)
        
        logger.info(f"Amazon Q CLI chat completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            raw_output = result.stdout.strip()
            clean_output = clean_ansi_codes(raw_output)
            
            if clean_output:
                logger.info("Amazon Q chat response received successfully")
                return True, clean_output
            else:
                return False, "Amazon Q returned an empty response"
        else:
            error_msg = result.stderr.strip()
            logger.error(f"Amazon Q CLI chat error: {error_msg}")
            
            if "not logged in" in error_msg.lower():
                return False, "Authentication required. Please login to Amazon Q CLI."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return False, "Amazon Q usage limit reached. Please try again later."
            else:
                return False, f"Amazon Q error: {clean_ansi_codes(error_msg)}"
                
    except subprocess.TimeoutExpired:
        logger.error("Amazon Q CLI chat request timed out")
        return False, "Request timed out. Please try again with a shorter message."
    except FileNotFoundError:
        logger.error("Amazon Q CLI not found")
        return False, "Amazon Q CLI not found. Please ensure it's installed and configured."
    except Exception as e:
        logger.error(f"Error in Amazon Q chat: {str(e)}")
        return False, f"Error in Amazon Q chat: {str(e)}"
```

### UI 整合

在 Streamlit 側邊欄中提供了完整的 Amazon Q CLI 管理界面：

```python
with st.sidebar:
    st.header("🤖 Amazon Q CLI")
    
    # 檢查當前狀態
    q_available, q_status = check_amazon_q_availability()
    
    if q_available:
        st.success(f"✅ Status: {q_status}")
        
        # 登出按鈕
        if st.button("🚪 Logout from Amazon Q"):
            with st.spinner("Logging out from Amazon Q..."):
                logout_success, logout_message = amazon_q_logout()
                if logout_success:
                    st.success(logout_message)
                    st.rerun()  # 重新整理狀態
                else:
                    st.error(logout_message)
    else:
        st.warning(f"⚠️ Status: {q_status}")
        
        # 登入按鈕
        if st.button("🔑 Login to Amazon Q"):
            with st.spinner("Opening browser for Amazon Q login..."):
                login_success, login_message = amazon_q_login()
                if login_success:
                    st.success(login_message)
                    st.rerun()  # 重新整理狀態
                else:
                    st.error(login_message)
```

## 使用方式

### 1. 自動登入流程

1. **檢查狀態**: 程式會自動檢測 Amazon Q CLI 的安裝和認證狀態
2. **顯示登入按鈕**: 如果未登入，側邊欄會顯示 "🔑 Login to Amazon Q" 按鈕
3. **點擊登入**: 點擊按鈕後，程式會執行 `q auth login` 命令
4. **瀏覽器認證**: 系統會自動開啟瀏覽器進行 AWS 認證
5. **完成登入**: 認證完成後，程式會更新狀態並顯示成功訊息

### 2. 登出流程

1. **顯示登出按鈕**: 如果已登入，側邊欄會顯示 "🚪 Logout from Amazon Q" 按鈕
2. **點擊登出**: 點擊按鈕後，程式會執行 `q auth logout` 命令
3. **完成登出**: 登出完成後，程式會更新狀態

### 3. 互動式聊天使用

1. **開啟聊天界面**: 在主界面中找到 Amazon Q 聊天區域
2. **輸入問題**: 在文字輸入框中輸入您想詢問的問題
3. **獲得回應**: Amazon Q 會根據您的數據上下文提供相關的分析和建議
4. **持續對話**: 可以進行多輪對話，深入探討數據洞察

### 4. 手動登入備案

如果自動登入失敗，程式提供了手動登入的說明：

```bash
# 在終端機中執行
q auth login

# 或者如果需要安裝 CLI
curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh
```

## 錯誤處理

### 常見錯誤和解決方案

1. **"Amazon Q CLI not installed"**
   - 解決方案: 安裝 Amazon Q CLI
   - 命令: `curl -sSL https://d2yblsmsllhwuq.cloudfront.net/q/install | sh`

2. **"Login timed out"**
   - 解決方案: 重試或手動在終端機中登入
   - 可能原因: 網路連線問題或瀏覽器認證超時

3. **"Authentication issue"**
   - 解決方案: 檢查 AWS 帳戶權限和 Amazon Q 存取權限
   - 可能需要聯繫 AWS 管理員

4. **"Not logged in"**
   - 解決方案: 點擊登入按鈕或手動執行 `q auth login`

5. **"Request timed out"**
   - 解決方案: 嘗試使用較短的訊息或檢查網路連線
   - 聊天請求有 45 秒的超時限制

6. **"Amazon Q usage limit reached"**
   - 解決方案: 等待一段時間後再試，或聯繫 AWS 管理員增加配額

7. **"Status check timed out"**
   - 解決方案: 檢查網路連線，重新整理頁面重試
   - 新的檢測機制會在超時後仍嘗試提供部分狀態資訊

8. **"Available (chat test failed but CLI detected)"**
   - 狀態說明: CLI 已安裝且可能已登入，但聊天功能可能有問題
   - 解決方案: 嘗試手動執行 `q chat "hello"` 測試，或重新登入

9. **"Available (chat test timed out but CLI detected)"**
   - 狀態說明: CLI 可用但網路回應較慢
   - 解決方案: 網路狀況改善後功能應正常，可嘗試較短的聊天訊息

## 安全考量

### 1. 認證流程
- 使用 AWS 官方的 OAuth 認證流程
- 不會在程式中儲存任何認證資訊
- 認證資訊由 Amazon Q CLI 安全管理

### 2. 權限管理
- 需要適當的 AWS IAM 權限才能使用 Amazon Q
- 建議使用最小權限原則

### 3. 日誌記錄
- 所有 Amazon Q CLI 操作都會記錄在 `amazon_q_cli.log` 中
- 不會記錄敏感的認證資訊

## 疑難排解

**📖 完整的安裝和疑難排解指南：**
- **[WSL/Linux 安裝指南](amazon-q-cli-installation.md)** - 359 行綜合 WSL 和 Linux 環境指南
- **[Windows & WSL 安裝指南](amazon-q-cli-windows-wsl.md)** - 基於 AWS 官方 blog 的 Windows 和 WSL 詳細指南

綜合安裝指南提供：

### 🔧 完整安裝方法
- **官方安裝腳本**: 自動化安裝和配置流程
- **手動下載方式**: 適用於企業或受限環境
- **用戶目錄安裝**: 無需管理員權限的安裝選項
- **網路問題解決**: 代理、DNS、防火牆配置

### 🖥️ WSL 專用指導
- **環境配置**: WSL 特定的路徑和權限設定
- **瀏覽器整合**: Windows 與 WSL 間的認證流程
- **系統整合**: 與 CHI Analyzer 的完整整合步驟
- **性能優化**: WSL 環境下的最佳實務

### 🛠️ 詳細疑難排解
- **常見錯誤診斷**: 逐步解決方案和根本原因分析
- **網路連接問題**: 企業環境和代理配置
- **認證流程**: 登入/登出管理和狀態驗證
- **版本兼容性**: 不同 CLI 版本的命令格式差異

### 快速檢查步驟

#### 檢查 CLI 安裝
```bash
q --version
```

#### 檢查認證狀態
```bash
q auth status
```

#### 測試連線
```bash
q chat "hello"
```

#### 查看日誌
檢查 `amazon_q_cli.log` 檔案以獲取詳細的錯誤資訊。

### 🔒 安全和最佳實務

詳細的安全考量，包括：
- **認證資訊管理**: 安全的憑證儲存和保護
- **權限配置**: IAM 權限和最小權限原則
- **網路安全**: HTTPS 連接和企業安全要求
- **日誌管理**: 安全的日誌記錄和監控

請參閱安裝指南獲取完整的安裝、配置和疑難排解指南：
- [WSL/Linux 安裝指南](amazon-q-cli-installation.md) - 詳細的 WSL 和 Linux 環境設定
- [Windows & WSL 安裝指南](amazon-q-cli-windows-wsl.md) - Windows 環境專用指南

## 最佳實務

1. **定期檢查狀態**: 程式會自動檢查認證狀態，但建議定期手動檢查
2. **網路連線**: 確保有穩定的網路連線進行認證
3. **權限管理**: 確保 AWS 帳戶有適當的 Amazon Q 存取權限
4. **版本更新**: 定期更新 Amazon Q CLI 到最新版本

## 技術細節

### 命令執行
程式使用 Python 的 `subprocess` 模組來執行 Amazon Q CLI 命令：

```python
# 登入命令
subprocess.run(['q', 'auth', 'login'], capture_output=True, text=True, timeout=60)

# 登出命令  
subprocess.run(['q', 'auth', 'logout'], capture_output=True, text=True, timeout=30)

# 狀態檢查
subprocess.run(['q', '--version'], capture_output=True, text=True, timeout=5)

# 聊天請求
subprocess.run(['q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt], 
               capture_output=True, text=True, timeout=45)
```

### 超時設定
- 登入操作: 60 秒超時
- 登出操作: 30 秒超時
- 狀態檢查: 5 秒超時（登入檢查）、3 秒超時（幫助命令）、8 秒超時（聊天測試）
- 聊天請求: 45 秒超時

### 錯誤捕獲
程式會捕獲並處理各種可能的錯誤情況，包括：
- 命令執行失敗
- 網路超時
- CLI 未安裝
- 認證失敗

## 聊天功能特色

### 1. 上下文感知
- 聊天功能會自動包含當前分析的數據上下文
- Amazon Q 可以基於您上傳的 CHI 數據提供相關建議
- 支援多輪對話，保持上下文連貫性

### 2. 智能分析建議
- 詢問特定客戶的安全分數趨勢
- 獲得改善建議和最佳實務
- 理解數據模式和異常情況

### 3. 即時互動
- 無需離開應用程式界面
- 快速獲得 AI 驅動的洞察
- 支援自然語言查詢

### 使用範例

```
使用者: "為什麼客戶 ABC Corp 的安全分數下降了？"
Amazon Q: "根據數據分析，ABC Corp 的安全分數從 65 下降到 38，主要原因可能包括..."

使用者: "我應該如何幫助 Return Back to Red 類別的客戶？"
Amazon Q: "對於 Return Back to Red 類別的客戶，建議採取以下行動..."
```

這個整合設計讓使用者可以在不離開 Web 界面的情況下完成 Amazon Q CLI 的認證管理和即時 AI 諮詢，大大提升了使用體驗和數據分析效率。
## 
新增功能詳解

### 1. 增強的摘要生成功能

#### 智能數據分析
```python
def generate_ai_summary(analysis_data: Dict) -> tuple[bool, str]:
    """Generate AI-powered summary using Amazon Q CLI with enhanced context"""
    
    # 包含完整的分析上下文
    analysis_context = {
        'exit_from_red': counts["Exit from Red"],
        'return_back_red': counts["Return Back to Red"],
        'new_comer_red': counts["New Comer to Red"],
        'missing_from_chi': counts["Missing from CHI"],
        'total_customers': total_customers,
        'prev_month_low_total': low_score_metrics['prev_month_low_total'],
        'curr_month_low_total': low_score_metrics['curr_month_low_total'],
        'low_score_improvement_count': low_score_metrics['improvement_count'],
        'low_score_improvement_pct': low_score_metrics['improvement_percentage']
    }
```

#### 專業報告格式
- **結構化提示**: 包含具體的分析數據和指標
- **專業語調**: 適合 TAM 團隊的正式報告格式
- **限制字數**: 200-300 字的簡潔專業摘要
- **避免格式問題**: 清理終端顏色代碼和格式化字符

### 2. 互動式聊天系統

#### 聊天歷史管理
```python
# 在 session state 中維護聊天記錄
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 顯示歷史對話
for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
    with st.expander(f"💬 Chat {i+1}: {user_msg[:50]}..."):
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Amazon Q:** {ai_response}")
```

#### 預定義快速問題
- **📈 Focus on improvements**: 強調正面趨勢和成功案例
- **⚠️ Highlight risks**: 突出安全風險和需要關注的領域
- **📊 Add more metrics**: 增加詳細指標和統計分析

#### 上下文感知對話
```python
analysis_context = f"""
Current CHI Analysis Data:
- Exit from Red: {analysis_data['exit_from_red']} customers
- Return Back to Red: {analysis_data['return_back_red']} customers  
- New Comer to Red: {analysis_data['new_comer_red']} customers
- Missing from CHI: {analysis_data['missing_from_chi']} customers
- Total customers: {analysis_data['total_customers']}
- Improvement: {analysis_data['low_score_improvement_pct']:.1f}%

Current AI Summary:
{ai_summary}
"""
```

### 3. 歷史趨勢分析

#### 自動數據提取
```python
def extract_historical_data(xls: pd.ExcelFile, threshold: float = 42) -> pd.DataFrame:
    """Extract historical trend data from all sheets in the Excel file"""
    
    # 自動檢測日期格式的工作表
    date_sheets = []
    for sheet in sheet_names:
        if re.match(r'\d{4}-\d{2}-\d{2}', sheet):
            date_sheets.append((pd.to_datetime(sheet), sheet))
    
    # 按時間順序排序
    date_sheets.sort(key=lambda x: x[0])
```

#### 互動式趨勢圖表
- **多線圖表**: 低分客戶數量、退出紅區、返回紅區的趨勢
- **懸停資訊**: 詳細的月度數據顯示
- **趨勢註解**: 最新月份的變化標註
- **顏色編碼**: 紅色（風險）、綠色（改善）、橙色（關注）

### 4. 增強的 PDF 報告

#### 專業版面設計
```python
def export_pdf(tables: Dict[str, pd.DataFrame], summary_df: pd.DataFrame, 
               analysis_summary: str = "", ai_summary: str = "") -> bytes:
    """Export analysis results to PDF format with rich web-like layout"""
    
    # A4 直向格式，專業邊距
    doc = SimpleDocTemplate(output, pagesize=A4, 
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
```

#### 豐富的視覺元素
- **彩色指標儀表板**: 帶有百分比和趨勢指示的執行摘要
- **表情符號圖標**: 增強視覺識別和專業外觀
- **顏色編碼表格**: 不同類別使用不同的顏色主題
- **AI 洞察高亮**: 特殊格式顯示 AI 生成的內容

### 5. 智能登入管理

#### 命令格式檢測
```python
def detect_q_cli_commands() -> dict:
    """Detect available Amazon Q CLI commands and their format"""
    try:
        # 檢查幫助輸出以確定命令結構
        help_result = subprocess.run(['q', '--help'], capture_output=True, text=True, timeout=5)
        help_text = help_result.stdout.lower()
        
        commands = {
            'login': ['q', 'login'],  # 預設為簡單命令
            'logout': ['q', 'logout'],
            'test': ['q', 'chat', 'hello']
        }
        
        # 根據幫助文本調整命令模式
        if 'auth' in help_text and 'login' in help_text:
            commands['login'] = ['q', 'auth', 'login']
            commands['logout'] = ['q', 'auth', 'logout']
            
        return commands
```

#### 優雅的錯誤處理
- **版本檢測**: 自動檢測 CLI 版本和可用命令
- **超時管理**: 不同操作使用適當的超時設定
- **錯誤分類**: 區分安裝、認證、網路等不同類型的錯誤
- **用戶指導**: 提供具體的解決步驟和建議

## 使用範例和最佳實務

### 聊天互動範例
```
使用者: "這個月的整體趨勢如何？"
Amazon Q: "根據分析，本月共有 15 位客戶退出紅區，顯示 23% 的改善率。然而，也有 8 位客戶返回紅區，需要重點關注..."

使用者: "請重寫摘要，更加強調成功案例"
Amazon Q: "已重新撰寫摘要，突出了客戶改善的積極趨勢和 TAM 團隊的成功協作..."

使用者: "為 Return Back to Red 的客戶提供具體建議"
Amazon Q: "建議對這些客戶採取以下行動：1) 立即安排一對一會議... 2) 檢查最近的配置變更... 3) 提供額外的安全培訓資源..."
```

### 工作流程最佳實務
1. **上傳數據**: 確保 Excel 檔案包含多個日期工作表以獲得完整趨勢分析
2. **檢查狀態**: 使用側邊欄的狀態指示器確認 Amazon Q 可用性
3. **生成摘要**: 先生成標準摘要，再使用 AI 增強功能
4. **互動改進**: 使用聊天功能根據具體需求調整摘要
5. **匯出報告**: 選擇適合的格式（Excel 用於數據分析，PDF 用於正式報告）

### 故障排除指南

#### 常見問題解決
1. **聊天功能無回應**
   - 檢查網路連線
   - 確認 Amazon Q 配額未超限
   - 嘗試較短的訊息

2. **摘要生成失敗**
   - 檢查認證狀態
   - 查看 `amazon_q_cli.log` 詳細錯誤
   - 重新登入 Amazon Q

3. **PDF 匯出問題**
   - 確認 reportlab 已安裝
   - 檢查系統記憶體是否充足
   - 嘗試較小的數據集

4. **歷史趨勢無數據**
   - 確保 Excel 檔案包含日期格式的工作表
   - 檢查工作表命名格式 (YYYY-MM-DD)
   - 驗證數據完整性

這個全面的整合設計提供了從數據上傳到最終報告生成的完整工作流程，大大提升了 TAM 團隊的工作效率和分析品質。