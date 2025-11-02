#!/bin/bash

echo "🚀 設置 Git Repository 並推送到 GitHub"
echo "========================================="

# 檢查是否已經是 git repository
if [ -d ".git" ]; then
    echo "⚠️  已存在 .git 目錄"
    read -p "是否要重新初始化? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
        echo "✅ 已清除舊的 git 配置"
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

# 初始化 git repository
echo "📁 初始化 Git repository..."
git init

# 設置 remote origin
echo "🔗 添加 remote repository..."
git remote add origin git@github.com:alegriaw/chi-monthly-report-analyzer.git

# 創建 .gitignore (如果不存在或需要更新)
echo "📝 更新 .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
chi_analyzer_env/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
*.log.*
amazon_q_cli.log*

# Temporary files
*.tmp
*.temp
*~

# Generated files
ai_summary_*.md
*.pdf
*.xlsx
*.Zone.Identifier

# Test files
test_*.py
debug*.py
simulate*.py
validate*.py

# Amazon Q
q/
q.zip

# WSL specific
*.bat
EOF

# 添加所有文件
echo "📦 添加文件到 staging..."
git add .

# 創建初始 commit
echo "💾 創建初始 commit..."
git commit -m "Initial commit: CHI Monthly Report Analyzer v2.0.7

- Complete Streamlit-based CHI security score analyzer
- AI-powered summary generation with Amazon Q CLI integration
- Interactive chat interface with conversation history
- Enhanced PDF export with chat history documentation
- Multi-sheet Excel report generation
- Historical trend analysis with Plotly visualizations
- WSL deployment scripts and comprehensive documentation
- Testing framework and debugging tools"

# 設置主分支
echo "🌿 設置主分支..."
git branch -M main

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
echo ""
echo "⚠️  注意: 請確保您已經:"
echo "   1. 登入 GitHub (https://github.com/alegriaw)"
echo "   2. 設置 SSH key 或使用 GitHub CLI"
echo "   3. Repository 'chi-monthly-report-analyzer' 已創建"
echo ""
read -p "按 Enter 繼續推送，或 Ctrl+C 取消..."

if git push -u origin main; then
    echo ""
    echo "🎉 成功推送到 GitHub!"
    echo "📍 Repository URL: https://github.com/alegriaw/chi-monthly-report-analyzer"
    echo ""
    echo "📋 後續步驟:"
    echo "   1. 訪問: https://github.com/alegriaw/chi-monthly-report-analyzer"
    echo "   2. 檢查文件是否正確上傳"
    echo "   3. 設置 repository 描述和 README"
    echo "   4. 考慮設置 GitHub Pages (如果需要)"
else
    echo ""
    echo "❌ 推送失敗"
    echo ""
    echo "🔧 可能的解決方案:"
    echo "   1. 檢查 SSH key: ssh -T git@github.com"
    echo "   2. 使用 HTTPS: git remote set-url origin https://github.com/alegriaw/chi-monthly-report-analyzer.git"
    echo "   3. 使用 GitHub CLI: gh auth login"
    echo "   4. 檢查 repository 是否存在"
fi