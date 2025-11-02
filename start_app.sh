#!/bin/bash
cd "$(dirname "$0")"

# 顯示當前目錄
echo "📁 當前目錄: $(pwd)"

# 檢查虛擬環境
if [ ! -d "chi_analyzer_env" ]; then
    echo "❌ 虛擬環境不存在，正在創建..."
    python3 -m venv chi_analyzer_env
fi

# 啟動虛擬環境
echo "🔄 啟動虛擬環境..."
source chi_analyzer_env/bin/activate

# 顯示 Python 路徑
echo "🐍 Python 路徑: $(which python)"

# 安裝依賴項
echo "📦 安裝依賴項..."
pip install --upgrade pip
pip install streamlit pandas openpyxl plotly reportlab

# 測試 reportlab
echo "🧪 測試 reportlab..."
python -c "
try:
    from reportlab.lib.pagesizes import A4
    print('✅ reportlab 測試成功')
except ImportError as e:
    print(f'❌ reportlab 測試失敗: {e}')
"

# 啟動應用程式
echo "🚀 啟動 Streamlit 應用程式..."
streamlit run chi_low_security_score_analyzer.py --server.port 8501