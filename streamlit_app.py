"""
WaterBuddy Setup Script
Quick setup for local development
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        "streamlit_app.py",
        "requirements.txt",
        ".streamlit/config.toml"
    ]
    
    print("\n📁 Checking required files...")
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
            all_exist = False
    
    return all_exist

def run_app():
    """Run the Streamlit app"""
    print("\n🚀 Starting WaterBuddy...")
    print("   The app will open in your browser automatically")
    print("   Press Ctrl+C to stop the app\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using WaterBuddy!")
    except Exception as e:
        print(f"\n❌ Error running app: {e}")

def main():
    """Main setup function"""
    print("=" * 50)
    print("🌊 WaterBuddy Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\n❌ Some required files are missing.")
        print("   Make sure you have all files from the repository.")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Ask to run app
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("=" * 50)
    
    response = input("\nWould you like to run WaterBuddy now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_app()
    else:
        print("\n📝 To run WaterBuddy later, use:")
        print("   streamlit run streamlit_app.py")
        print("\n👋 Happy hydrating!")

if __name__ == "__main__":
    main()
