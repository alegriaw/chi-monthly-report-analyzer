# GenAI Report 與 Amazon Q CLI Session 處理機制

## 概述

CHI Low Security Score Analyzer 中的 GenAI 報告和 Amazon Q CLI 會話管理是一個複雜的系統，涉及狀態管理、會話持久性、和多輪對話處理。以下是詳細的技術說明。

## 系統架構

### 1. **狀態管理層次**

```
Streamlit Session State (持久層)
├── original_ai_summary      # 原始 AI 摘要
├── improved_summary         # 改進後的摘要
├── ai_summary_generated     # 生成狀態標記
├── chat_history            # 聊天記錄
├── pending_quick_question  # 待處理問題
└── ai_summary_error        # 錯誤訊息
```

### 2. **處理流程**

```
用戶操作 → 狀態檢查 → AI 生成/緩存 → 聊天互動 → 狀態更新 → UI 顯示
```

## GenAI Report 處理機制

### 1. **AI 摘要生成控制**

```python
# 關鍵邏輯：只生成一次，之後使用緩存
if "original_ai_summary" not in st.session_state:
    print("🔍 DEBUG: Generating NEW AI summary...")
    success, ai_summary = generate_ai_summary(analysis_data)
    if success:
        st.session_state.original_ai_summary = ai_summary
        st.session_state.ai_summary_generated = True
else:
    # 使用緩存的 AI 摘要
    success = st.session_state.ai_summary_generated
    ai_summary = st.session_state.original_ai_summary
```

**關鍵特點：**
- **一次生成原則**: 避免重複調用 Amazon Q CLI
- **狀態持久化**: 使用 `st.session_state` 保存結果
- **錯誤處理**: 分別處理成功和失敗狀態

### 2. **摘要版本管理**

```python
# 顯示邏輯：優先顯示改進版本
display_summary = st.session_state.get('improved_summary', ai_summary)

# 版本指示器
if 'improved_summary' in st.session_state:
    st.info("📝 **Showing improved summary** (modified by Amazon Q Chat)")
else:
    st.info("📝 **Showing original AI summary**")
```

**版本控制功能：**
- **原始版本**: `original_ai_summary` - 永不改變
- **改進版本**: `improved_summary` - 可多次更新
- **顯示邏輯**: 優先顯示改進版本
- **回退功能**: 可以回到原始版本

### 3. **UI 可見性控制**

```python
# 智能顯示邏輯
show_ai_section = (use_ai and q_available) or \
                 ("original_ai_summary" in st.session_state and 
                  st.session_state.get("ai_summary_generated", False))
```

**可見性規則：**
- **首次顯示**: 用戶點擊生成按鈕
- **持續顯示**: 已有生成的摘要
- **避免消失**: 按鈕點擊後界面不會重置

## Amazon Q CLI Session 管理

### 1. **會話狀態檢查**

```python
def check_amazon_q_availability() -> tuple[bool, str]:
    # 使用緩存避免頻繁檢查
    if cache_valid():
        return cached_result
    
    # 快速登入狀態檢查
    login_check = subprocess.run(['q', 'login'], ...)
    if "already logged in" in login_check.stderr.lower():
        return True, "Available and authenticated"
```

**檢查策略：**
- **緩存機制**: 5 分鐘內不重複檢查
- **快速檢查**: 使用 `q login` 而非 `q chat`
- **狀態緩存**: 避免 UI 阻塞

### 2. **聊天會話管理**

```python
# 聊天記錄結構
st.session_state.chat_history = [
    (question1, response1),
    (question2, response2),
    ...
]

# 會話持久性
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
```

**會話特點：**
- **累積記錄**: 保存所有對話
- **結構化存儲**: (問題, 回應) 元組
- **跨重新運行**: Streamlit 重新運行時保持

### 3. **上下文管理**

```python
def get_chat_context():
    # 使用當前顯示的摘要作為上下文
    current_summary = st.session_state.get('improved_summary', 
                     st.session_state.get('original_ai_summary', ai_summary))
    
    # 優化上下文長度
    if len(current_summary) > 2000:
        summary_for_context = current_summary[:2000] + "\n\n[Summary truncated...]"
    
    # 簡化格式減少處理時間
    context = f"""CHI Analysis: {analysis_data['exit_from_red']} improved, ...
Current Summary:
{summary_for_context}"""
```

**上下文策略：**
- **動態生成**: 每次調用時生成最新上下文
- **當前摘要**: 使用用戶當前看到的版本
- **長度優化**: 超過 2000 字符自動截斷
- **格式簡化**: 減少不必要的格式化

## 按鈕互動處理

### 1. **延遲處理模式**

```python
# 按鈕點擊：設置待處理狀態
if st.button("📈 Focus on improvements"):
    st.session_state.pending_quick_question = "Please rewrite..."
    st.rerun()

# 重新運行後：處理待處理問題
if st.session_state.pending_quick_question:
    question = st.session_state.pending_quick_question
    st.session_state.pending_quick_question = None  # 立即清除
    # 處理問題...
```

**處理流程：**
1. **按鈕點擊** → 設置 `pending_quick_question`
2. **觸發重新運行** → `st.rerun()`
3. **檢查待處理** → 處理問題並清除狀態
4. **顯示結果** → 更新 UI

### 2. **狀態同步**

```python
# 確保狀態一致性
chat_success, chat_response = chat_with_amazon_q(question, get_chat_context())

if chat_success:
    # 添加到聊天記錄
    st.session_state.chat_history.append((question, chat_response))
    
    # 用戶選擇應用改進
    if st.button("🔄 Use this as new summary"):
        st.session_state.improved_summary = chat_response
        st.rerun()
```

## 多輪對話支持

### 1. **上下文連續性**

```python
# 每次對話都基於當前顯示的摘要
current_summary = st.session_state.get('improved_summary', 
                 st.session_state.get('original_ai_summary'))

# 支持基於改進版本的進一步改進
context = f"Current Summary: {current_summary}"
```

**連續性保證：**
- **當前狀態**: 總是使用最新的摘要版本
- **改進鏈**: 支持 A → B → C 的多輪改進
- **上下文更新**: 每次對話都包含最新內容

### 2. **會話歷史管理**

```python
# 顯示聊天記錄
if st.session_state.chat_history:
    for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
        with st.expander(f"💬 Chat {i+1}: {user_msg[:50]}..."):
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**Amazon Q:** {ai_response}")

# 清除功能
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
```

## 錯誤處理和恢復

### 1. **超時處理**

```python
# 增加超時時間並優化上下文
result = subprocess.run([
    'q', 'chat', '--no-interactive', '--trust-all-tools', full_prompt
], capture_output=True, text=True, timeout=90)  # 90 秒超時
```

### 2. **狀態恢復**

```python
# 重新生成功能
if st.button("🔄 Regenerate"):
    # 清除所有相關狀態
    for key in ['original_ai_summary', 'improved_summary', 
                'ai_summary_generated', 'chat_history']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
```

### 3. **錯誤狀態管理**

```python
# 分離成功和錯誤狀態
if success:
    st.session_state.ai_summary_generated = True
    st.session_state.original_ai_summary = ai_summary
else:
    st.session_state.ai_summary_generated = False
    st.session_state.ai_summary_error = ai_summary
```

## 性能優化

### 1. **緩存策略**

- **AI 摘要**: 只生成一次，永久緩存
- **Q CLI 狀態**: 5 分鐘緩存 (詳見 [Cache Duration Analysis](cache-duration-analysis.md) 了解緩存時間優化分析)
- **聊天記錄**: 會話級緩存

### 2. **上下文優化**

- **長度限制**: 超過 2000 字符截斷
- **格式簡化**: 移除不必要的格式化
- **數據壓縮**: 只包含關鍵信息

### 3. **UI 響應性**

- **延遲處理**: 避免阻塞 UI
- **狀態指示**: 清楚顯示當前狀態
- **進度反饋**: 使用 spinner 和狀態訊息

## 調試和監控

### 1. **Debug 輸出**

```python
print(f"🔍 DEBUG: Using CACHED AI summary. Success: {success}")
print(f"🔍 DEBUG: Display summary length: {len(display_summary)} chars")
print(f"🔍 DEBUG: Chat history has {len(st.session_state.chat_history)} items")
```

### 2. **狀態追蹤**

- **生成狀態**: 追蹤 AI 摘要生成
- **會話狀態**: 監控聊天記錄
- **錯誤狀態**: 記錄失敗原因

這個系統設計確保了 GenAI 報告和 Amazon Q CLI 會話的穩定性、持久性和用戶友好性，支持複雜的多輪對話和狀態管理需求。