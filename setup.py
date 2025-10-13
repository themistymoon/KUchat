"""
KUchat Setup Script
Automated setup for Multi-Modal AI Chatbot with RAG System
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("  🎓 KUchat - Multi-Modal AI Chatbot Setup")
    print("  Kasetsart University Curriculum Chatbot")
    print("="*70 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected\n")

def create_venv():
    """Create virtual environment"""
    print("📦 Creating virtual environment...")
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("   Do you want to recreate it? (y/n): ").lower()
        if response == 'y':
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("✅ Using existing virtual environment\n")
            return
    
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("✅ Virtual environment created\n")

def get_pip_command():
    """Get the correct pip command for the platform"""
    if sys.platform == "win32":
        return str(Path("venv") / "Scripts" / "pip.exe")
    else:
        return str(Path("venv") / "bin" / "pip")

def install_requirements():
    """Install Python dependencies"""
    print("📥 Installing dependencies...")
    print("   This may take a few minutes...\n")
    
    pip_cmd = get_pip_command()
    
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("\n✅ Dependencies installed successfully\n")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_config_template():
    """Create configuration template"""
    print("📝 Creating configuration template...")
    
    config_template = {
        "api_url": "YOUR_NGROK_URL_HERE",
        "frontend_port": 7860,
        "auto_open_browser": True,
        "notes": {
            "api_url": "Replace with your ngrok URL from Google Colab",
            "frontend_port": "Port for Gradio interface (7860 is default)",
            "auto_open_browser": "Set to false to disable automatic browser opening"
        }
    }
    
    config_file = Path("config.json")
    if not config_file.exists():
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_template, f, indent=2, ensure_ascii=False)
        print("✅ Config template created: config.json\n")
    else:
        print("⚠️  config.json already exists, skipping\n")

def create_colab_instructions():
    """Create Colab setup instructions file"""
    print("📋 Creating Colab setup guide...")
    
    instructions = """# 🚀 Google Colab Setup Instructions

## Step 1: Open in Colab
1. Go to https://colab.research.google.com/
2. Click "File" → "Upload notebook"
3. Upload `colab_backend.ipynb` from this repository

## Step 2: Set GPU
1. Click "Runtime" → "Change runtime type"
2. Select "A100 GPU" (requires Colab Pro Plus)
3. Click "Save"

## Step 3: Get Your Tokens

### HuggingFace Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it "KUchat" and select "Read" permission
4. Copy the token

### Ngrok Auth Token
1. Go to https://dashboard.ngrok.com/get-started/your-authtoken
2. Sign up/login (free account works)
3. Copy your auth token

## Step 4: Configure Notebook

### Find Cell 2 (after first markdown):
```python
# Add your tokens here:
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxx"  # Replace with your HuggingFace token
```

### Find the last cell (Ngrok setup):
```python
NGROK_AUTH_TOKEN = "your_ngrok_token_here"  # Replace with your Ngrok token
```

## Step 5: (Optional) Auto-Load Your Documents

### Option A: Upload to Colab
1. Click the folder icon on left sidebar
2. Create folder: `/content/docs`
3. Upload your PDFs to this folder
4. Maintain folder structure (e.g., `docs/Science/ComputerScience_65.pdf`)

### Option B: Use Google Drive (Recommended for many files)
1. Upload your `docs` folder to Google Drive
2. Add this cell BEFORE running the notebook:
```python
from google.colab import drive
drive.mount('/content/drive')
```
3. Update the auto-load path in the auto-load cell:
```python
auto_load_result = auto_load_documents_from_folder(
    rag_system, 
    "/content/drive/My Drive/KUchat/docs"  # Update this path
)
```

## Step 6: Run the Notebook
1. Click "Runtime" → "Run all"
2. Wait 5-10 minutes for models to load
3. Watch for "AUTO-LOADING DOCUMENTS" section
4. Look for this output:
```
🚀 SERVER STARTED SUCCESSFULLY!
📡 Public URL: https://xxxx-xx-xx-xxx-xxx.ngrok.io
```

## Step 7: Copy the Ngrok URL
**IMPORTANT:** Copy the URL that appears (e.g., `https://1234-56-78-90-12.ngrok.io`)

You'll need this for the frontend setup!

---

## ⚠️ Important Notes

- Keep the Colab tab open while using the chatbot
- The ngrok URL changes every time you restart Colab
- Free Colab has usage limits; Pro Plus recommended for A100 GPU
- Models take ~55-60GB VRAM, need A100 80GB GPU

## ✅ Success Indicators

You'll know it's working when you see:
- ✅ Models loaded successfully
- ✅ Documents auto-loaded (if you uploaded docs)
- ✅ FastAPI server running
- ✅ Ngrok tunnel established
- ✅ Public URL displayed

---

**Next:** Return to main README.md for frontend setup!
"""
    
    with open("COLAB_SETUP.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Colab guide created: COLAB_SETUP.md\n")

def update_frontend_with_config():
    """Create a new frontend starter script that uses config.json"""
    print("🔧 Creating smart frontend launcher...")
    
    launcher_script = '''"""
KUchat Frontend Launcher
Automatically loads configuration and starts the Gradio interface
"""

import json
import sys
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_file = Path("config.json")
    
    if not config_file.exists():
        print("❌ config.json not found!")
        print("   Please run setup.py first or create config.json manually")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config

def check_api_url(api_url):
    """Check if API URL is configured"""
    if api_url == "YOUR_NGROK_URL_HERE" or not api_url:
        print("\\n" + "="*70)
        print("⚠️  API URL NOT CONFIGURED!")
        print("="*70)
        print("\\nPlease update config.json with your ngrok URL from Google Colab.")
        print("\\nSteps:")
        print("1. Run colab_backend.ipynb in Google Colab")
        print("2. Copy the ngrok URL (e.g., https://xxxx-xxx.ngrok.io)")
        print("3. Edit config.json and replace YOUR_NGROK_URL_HERE")
        print("4. Run this script again")
        print("\\n" + "="*70 + "\\n")
        sys.exit(1)

def main():
    """Main launcher function"""
    print("\\n" + "="*70)
    print("  🚀 Starting KUchat Frontend")
    print("="*70 + "\\n")
    
    # Load configuration
    config = load_config()
    api_url = config.get("api_url", "")
    port = config.get("frontend_port", 7860)
    auto_open = config.get("auto_open_browser", True)
    
    # Check API URL
    check_api_url(api_url)
    
    print(f"📡 API URL: {api_url}")
    print(f"🌐 Frontend Port: {port}")
    print(f"🖥️  Auto-open Browser: {auto_open}")
    print()
    
    # Import and patch frontend_app
    import frontend_app
    
    # Override API_URL
    frontend_app.API_URL = api_url
    
    # Modify launch parameters
    original_demo = frontend_app.demo
    
    # Launch with config
    print("🎨 Launching Gradio interface...")
    print(f"📍 Open browser to: http://localhost:{port}")
    print("\\n⏸️  Press Ctrl+C to stop the server\\n")
    
    original_demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        inbrowser=auto_open
    )

if __name__ == "__main__":
    main()
'''
    
    with open("run_frontend.py", 'w', encoding='utf-8') as f:
        f.write(launcher_script)
    
    print("✅ Frontend launcher created: run_frontend.py\n")

def create_quick_start_scripts():
    """Create platform-specific quick start scripts"""
    print("📜 Creating quick start scripts...")
    
    # Windows script
    windows_script = '''@echo off
echo ========================================
echo   KUchat Frontend Quick Start
echo ========================================
echo.

REM Activate virtual environment
if exist venv\\Scripts\\activate.bat (
    call venv\\Scripts\\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python setup.py
    pause
    exit /b 1
)

REM Run frontend
python run_frontend.py

pause
'''
    
    with open("START.bat", 'w', encoding='utf-8') as f:
        f.write(windows_script)
    
    # Unix script
    unix_script = '''#!/bin/bash
echo "========================================"
echo "  KUchat Frontend Quick Start"
echo "========================================"
echo

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python setup.py"
    exit 1
fi

# Run frontend
python run_frontend.py
'''
    
    with open("start.sh", 'w', encoding='utf-8') as f:
        f.write(unix_script)
    
    # Make Unix script executable
    if sys.platform != "win32":
        os.chmod("start.sh", 0o755)
    
    print("✅ Quick start scripts created:")
    print("   - START.bat (Windows)")
    print("   - start.sh (Linux/Mac)\n")

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*70)
    print("  ✅ SETUP COMPLETE!")
    print("="*70 + "\n")
    
    print("📋 NEXT STEPS:\n")
    
    print("1️⃣  Setup Google Colab Backend:")
    print("   - Read COLAB_SETUP.md for detailed instructions")
    print("   - Upload colab_backend.ipynb to Google Colab")
    print("   - Add your HuggingFace and Ngrok tokens")
    print("   - Run all cells and copy the ngrok URL\n")
    
    print("2️⃣  Configure Frontend:")
    print("   - Edit config.json")
    print("   - Replace YOUR_NGROK_URL_HERE with your ngrok URL\n")
    
    print("3️⃣  Start Frontend:")
    if sys.platform == "win32":
        print("   - Double-click START.bat, OR")
        print("   - Run: .\\venv\\Scripts\\activate")
        print("          python run_frontend.py\n")
    else:
        print("   - Run: ./start.sh, OR")
        print("   - Run: source venv/bin/activate")
        print("          python run_frontend.py\n")
    
    print("📚 DOCUMENTATION:")
    print("   - README.md - Complete documentation")
    print("   - QUICKSTART.md - 5-minute setup guide")
    print("   - COLAB_SETUP.md - Colab setup instructions")
    print("   - DOCUMENT_LOADING_GUIDE.md - How to load your PDFs\n")
    
    print("🎓 YOUR CURRICULUM:")
    print("   - Add PDFs to docs/ folder")
    print("   - Upload to Google Drive")
    print("   - Auto-loads when Colab starts!\n")
    
    print("="*70)
    print("  🚀 Happy Chatting!")
    print("="*70 + "\n")

def main():
    """Main setup function"""
    try:
        print_banner()
        check_python_version()
        create_venv()
        install_requirements()
        create_config_template()
        create_colab_instructions()
        update_frontend_with_config()
        create_quick_start_scripts()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
