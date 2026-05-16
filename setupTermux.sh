#!/data/data/com.termux/files/usr/bin/bash
# =============================================
#   TeleBot Panel - Setup Script untuk Termux
# =============================================

echo ""
echo "  🤖 TeleBot Panel Setup"
echo "  ========================"
echo ""

# Update packages
echo "📦 Update packages..."
pkg update -y && pkg upgrade -y

# Install Python
echo "🐍 Install Python..."
pkg install python -y

# Install pip packages
echo "📥 Install dependencies..."
pip install flask flask-cors

echo ""
echo "✅ Setup selesai!"
echo ""
echo "  Cara guna:"
echo "  1. python server.py"
echo "  2. Buka browser: http://localhost:5000"
echo ""
