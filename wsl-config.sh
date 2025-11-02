#!/bin/bash

# WSL Configuration Script for CHI Low Security Score Analyzer
# This script sets up the WSL environment for optimal performance

echo "⚙️  WSL Configuration for CHI Low Security Score Analyzer"
echo "======================================================="

# Create WSL-specific configuration directory
mkdir -p ~/.config/chi-analyzer

# Create environment configuration
cat > ~/.config/chi-analyzer/wsl-env.conf << 'EOF'
# CHI Analyzer WSL Environment Configuration
export CHI_ANALYZER_ENV=wsl
export CHI_ANALYZER_HOST=0.0.0.0
export CHI_ANALYZER_PORT=8501
export CHI_ANALYZER_BROWSER=false
EOF

# Add to bashrc if not already present
if ! grep -q "chi-analyzer/wsl-env.conf" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# CHI Analyzer WSL Configuration" >> ~/.bashrc
    echo "if [ -f ~/.config/chi-analyzer/wsl-env.conf ]; then" >> ~/.bashrc
    echo "    source ~/.config/chi-analyzer/wsl-env.conf" >> ~/.bashrc
    echo "fi" >> ~/.bashrc
    echo "✅ Added configuration to ~/.bashrc"
fi

# Create systemd service file (if systemd is available)
if command -v systemctl &> /dev/null; then
    echo "🔧 Creating systemd service..."
    
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    sudo tee /etc/systemd/user/chi-analyzer.service > /dev/null << EOF
[Unit]
Description=CHI Low Security Score Analyzer
After=network.target

[Service]
Type=exec
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/chi_analyzer_env/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$PROJECT_DIR/chi_analyzer_env/bin/streamlit run chi_low_security_score_analyzer.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

    echo "✅ Systemd service created"
    echo "💡 To enable auto-start: systemctl --user enable chi-analyzer"
    echo "💡 To start service: systemctl --user start chi-analyzer"
fi

# Create desktop shortcut
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/CHI-Analyzer.desktop" << EOF
[Desktop Entry]
Version=2.0.2
Type=Application
Name=CHI Low Security Score Analyzer
Comment=Customer Health Index Security Score Analysis Tool
Exec=bash -c 'cd "$PROJECT_DIR" && ./deploy-wsl.sh'
Icon=applications-internet
Terminal=true
Categories=Office;Development;
EOF
    chmod +x "$HOME/Desktop/CHI-Analyzer.desktop"
    echo "✅ Desktop shortcut created"
fi

# Set up log rotation
sudo tee /etc/logrotate.d/chi-analyzer > /dev/null << 'EOF'
/home/*/Dev/Project/DevTAM/chi-monthly-report/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

echo "✅ Log rotation configured"

# Create alias for easy access
if ! grep -q "alias chi-analyzer" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# CHI Analyzer alias" >> ~/.bashrc
    echo "alias chi-analyzer='cd $PROJECT_DIR && ./deploy-wsl.sh'" >> ~/.bashrc
    echo "✅ Added 'chi-analyzer' alias to ~/.bashrc"
fi

echo ""
echo "🎉 WSL configuration completed!"
echo ""
echo "📋 Available commands:"
echo "   chi-analyzer          - Start the application"
echo "   ./deploy-wsl.sh       - Direct deployment script"
echo "   systemctl --user start chi-analyzer  - Start as service (if systemd available)"
echo ""
echo "🔄 Please run 'source ~/.bashrc' or restart your terminal to apply changes"