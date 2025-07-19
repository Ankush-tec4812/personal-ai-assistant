 @echo off
echo 🚀 Personal AI Assistant Setup
echo ================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo    Visit: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    echo    Visit: https://python.org/
    pause
    exit /b 1
)

echo ✅ Node.js and Python are installed

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
call npm install --legacy-peer-deps

if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Node.js dependencies installed

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd assistant

call pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    echo 💡 Try installing with: pip install --user -r requirements.txt
    echo    Or use conda: conda install pyaudio
    cd ..
    pause
    exit /b 1
)

cd ..

echo ✅ Python dependencies installed

REM Check for Firebase configuration
echo 🔥 Checking Firebase configuration...

if not exist ".env.local" (
    echo ❌ .env.local file not found
    echo 💡 Please create .env.local with your Firebase configuration
) else (
    findstr "your_api_key_here" .env.local >nul
    if %errorlevel% equ 0 (
        echo ⚠️  .env.local contains placeholder values
        echo 💡 Please update .env.local with your actual Firebase configuration
    ) else (
        echo ✅ .env.local configuration looks good
    )
)

if not exist "assistant\serviceAccountKey.json" (
    echo ❌ Firebase service account key not found
    echo 💡 Please place your serviceAccountKey.json in the assistant\ directory
) else (
    echo ✅ Firebase service account key found
)

echo.
echo 🎉 Setup Complete!
echo ===================
echo.
echo Next steps:
echo 1. Configure Firebase:
echo    - Update .env.local with your Firebase project details
echo    - Place serviceAccountKey.json in assistant\ directory
echo.
echo 2. Start the Next.js dashboard:
echo    npm run dev
echo.
echo 3. In another terminal, start the Python assistant:
echo    python assistant\assistant.py
echo.
echo 4. Start talking to your assistant!
echo.
echo 📚 For detailed instructions, see:
echo    - README.md (main documentation)
echo    - assistant\README.md (Python assistant details)
echo.
echo 🆘 Need help? Check the troubleshooting section in README.md

pause
