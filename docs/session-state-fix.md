# Session State 修復說明

## 問題描述

當用戶在 "Improve Summary with Amazon Q Chat" 功能中按下快速操作按鈕（如 "📈 Focus on improvements"）時，整個 GenAI Monthly Summary Report 會被重置，導致：

1. **AI 摘要消失**: 原始生成的 AI 摘要被重置
2. **聊天記錄丟失**: 之前的對話記錄可能消失
3. **用戶體驗差**: 需要重新生成摘要

## 根本原因

### Streamlit 重新運行機制

Streamlit 的工作原理是當用戶與界面互動時（如按鈕點擊），整個腳本會重新執行：

```python
# 問題代碼
if st.button("📈 Focus on improvements"):
    quick_question = "Please rewrite the summary..."
    # 立即處理，但會觸發重新運行
    chat_response = chat_with_amazon_q(quick_question, context)
    # 重新運行時，ai_summary 可能被重置
```

### 狀態丟失

1. **按鈕點擊** → 設置 `quick_question`
2. **開始處理** → 調用 Amazon Q
3. **Streamlit 重新運行** → 整個腳本重新執行
4. **狀態丟失** → `ai_summary` 和其他變數被重置

## 解決方案

### 1. 使用 Session State 保存狀態

```python
# 保存 AI 摘要到 session state
if "current_ai_summary" not in st.session_state or st.session_state.current_ai_summary != ai_summary:
    st.session_state.current_ai_summary = ai_summary

# 保存聊天記錄
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
```

### 2. 延遲處理機制

```python
# 新的處理方式
if st.button("📈 Focus on improvements"):
    # 不立即處理，而是設置待處理狀態
    st.session_state.pending_quick_question = "Please rewrite the summary..."
    st.rerun()  # 觸發重新運行

# 在重新運行後處理
if st.session_state.pending_quick_question:
    question = st.session_state.pending_quick_question
    st.session_state.pending_quick_question = None  # 立即清除
    
    # 使用保存的摘要
    current_summary = st.session_state.get('current_ai_summary', ai_summary)
    chat_response = chat_with_amazon_q(question, context_with_stored_summary)
```

### 3. 狀態一致性保證

```python
# 使用保存的摘要而不是當前變數
context_with_stored_summary = f"""
Current AI Summary:
{st.session_state.get('current_ai_summary', ai_summary)}
"""
```

## 修復的關鍵點

### 1. **狀態持久化**
- 將 AI 摘要保存到 `st.session_state.current_ai_summary`
- 將聊天記錄保存到 `st.session_state.chat_history`
- 將改進的摘要保存到 `st.session_state.improved_summary`

### 2. **延遲處理**
- 按鈕點擊時不立即處理，而是設置 `pending_quick_question`
- 在下一次運行時處理待處理的問題
- 處理完成後立即清除待處理狀態

### 3. **上下文一致性**
- 使用保存的 AI 摘要構建聊天上下文
- 確保 Amazon Q 看到的是正確的摘要內容

## 修復前後對比

### 修復前
```python
# ❌ 問題代碼
if st.button("📈 Focus on improvements"):
    quick_question = "Please rewrite..."
    # 立即處理，可能導致狀態丟失
    chat_response = chat_with_amazon_q(quick_question, analysis_context)
```

### 修復後
```python
# ✅ 修復代碼
if st.button("📈 Focus on improvements"):
    st.session_state.pending_quick_question = "Please rewrite..."
    st.rerun()

if st.session_state.pending_quick_question:
    question = st.session_state.pending_quick_question
    st.session_state.pending_quick_question = None
    
    # 使用保存的摘要
    current_summary = st.session_state.get('current_ai_summary', ai_summary)
    context = f"Current AI Summary: {current_summary}"
    chat_response = chat_with_amazon_q(question, context)
```

## 用戶體驗改進

### 1. **摘要持久性**
- ✅ AI 摘要不會在按鈕點擊後消失
- ✅ 改進的摘要會被正確保存和顯示
- ✅ 可以在原始和改進版本之間切換

### 2. **聊天記錄保持**
- ✅ 聊天記錄在整個會話中保持
- ✅ 可以查看之前的所有對話
- ✅ 支持清除聊天記錄功能

### 3. **狀態指示**
- ✅ 清楚顯示當前使用的是原始還是改進摘要
- ✅ 提供恢復到原始摘要的選項
- ✅ 顯示 Amazon Q 狀態

## 測試驗證

### 測試工具

#### 1. 基本測試腳本 (`test-session-state-fix.py`)
- **用途**: 驗證會話狀態持久性的基本功能
- **特點**: 模擬真實用戶互動模式
- **運行**: `streamlit run test-session-state-fix.py`

#### 2. 高級調試工具 (`debug-session-state.py`)
- **用途**: 深度調試會話狀態行為的互動式工具
- **特點**:
  - 實時會話狀態檢查和監控
  - 模擬 Amazon Q 回應，無需 CLI 依賴
  - 互動式快速操作按鈕，提供即時反饋
  - 聊天記錄可視化和管理
  - 上下文生成測試和驗證
  - 完整的會話狀態重置功能
- **運行**: `streamlit run debug-session-state.py`

### 測試步驟

#### 基本功能測試
1. 生成 AI 摘要
2. 點擊 "📈 Focus on improvements" 按鈕
3. 驗證摘要沒有被重置
4. 檢查聊天記錄是否保持
5. 測試改進摘要的保存和顯示

#### 高級調試測試
1. 運行 `debug-session-state.py`
2. 檢查當前會話狀態顯示
3. 測試快速操作按鈕（改進重點、風險突出、添加指標）
4. 驗證待處理問題的處理流程
5. 檢查模擬 Amazon Q 回應的生成
6. 測試摘要替換和改進工作流程
7. 驗證聊天記錄的累積和管理
8. 測試完整的會話狀態重置

### 預期結果
- ✅ AI 摘要保持不變
- ✅ Amazon Q 回應正確顯示
- ✅ 聊天記錄累積保存
- ✅ 可以正常使用改進的摘要
- ✅ 調試工具提供準確的狀態信息
- ✅ 模擬回應正確處理和顯示

## 技術細節

### Session State 變數
```python
st.session_state.current_ai_summary      # 當前 AI 摘要
st.session_state.improved_summary        # 改進的摘要
st.session_state.chat_history           # 聊天記錄
st.session_state.pending_quick_question # 待處理的快速問題
st.session_state.pending_custom_question # 待處理的自訂問題
```

### 處理流程
1. **初始化** → 設置所有必要的 session state 變數
2. **按鈕點擊** → 設置待處理狀態並觸發重新運行
3. **重新運行** → 檢查待處理狀態並處理
4. **結果顯示** → 使用保存的狀態顯示結果

這個修復確保了用戶在使用聊天改進功能時不會遇到狀態重置的問題，提供了流暢的用戶體驗。