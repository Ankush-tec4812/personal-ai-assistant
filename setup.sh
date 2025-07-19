#!/bin/bash

# Personal AI Assistant Setup Script
# This script helps you set up the Personal AI Assistant quickly

echo "🚀 Personal AI Assistant Setup"
echo "================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.7+ first."
    echo "   Visit: https://python.org/"
    exit 1
fi

echo "✅ Node.js and Python are installed"

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install --legacy-peer-deps

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

echo "✅ Node.js dependencies installed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd assistant

# Try to use python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found"
    exit 1
fi

# Check if pip is available
if ! command -v $PIP_CMD &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    echo "💡 Try installing system dependencies first:"
    echo "   macOS: brew install portaudio"
    echo "   Ubuntu/Debian: sudo apt-get install python3-pyaudio portaudio19-dev"
    echo "   Or use conda: conda install pyaudio"
    exit 1
fi

cd ..

echo "✅ Python dependencies installed"

# Check for Firebase configuration
echo "🔥 Checking Firebase configuration..."

if [ ! -f ".env.local" ]; then
    echo "❌ .env.local file not found"
    echo "💡 Please create .env.local with your Firebase configuration"
else
    # Check if .env.local has placeholder values
    if grep -q "your_api_key_here" .env.local; then
        echo "⚠️  .env.local contains placeholder values"
        echo "💡 Please update .env.local with your actual Firebase configuration"
    else
        echo "✅ .env.local configuration looks good"
    fi
fi

if [ ! -f "assistant/serviceAccountKey.json" ]; then
    echo "❌ Firebase service account key not found"
    echo "💡 Please place your serviceAccountKey.json in the assistant/ directory"
else
    echo "✅ Firebase service account key found"
fi

echo ""
echo "🎉 Setup Complete!"
echo "==================="
echo ""
echo "Next steps:"
echo "1. Configure Firebase:"
echo "   - Update .env.local with your Firebase project details"
echo "   - Place serviceAccountKey.json in assistant/ directory"
echo ""
echo "2. Start the Next.js dashboard:"
echo "   npm run dev"
echo ""
echo "3. In another terminal, start the Python assistant:"
echo "   $PYTHON_CMD assistant/assistant.py"
echo ""
echo "4. Start talking to your assistant!"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - README.md (main documentation)"
echo "   - assistant/README.md (Python assistant details)"
echo ""
echo "🆘 Need help? Check the troubleshooting section in README.md"
