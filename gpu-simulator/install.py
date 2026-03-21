"""
Installation script for GPU Parallel Floating-Point Simulator
Handles dependency installation with fallback options
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def install_dependencies():
    """Install dependencies with fallback options"""
    print("🚀 Installing GPU Parallel Floating-Point Simulator Dependencies\n")
    
    # First, try to upgrade pip and install setuptools
    print("📦 Updating pip and setuptools...")
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    run_command("python -m pip install --upgrade setuptools wheel", "Installing setuptools and wheel")
    
    # Try installing dependencies one by one with fallbacks
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn[standard]", "ASGI server"),
        ("numpy", "Numerical computing library"),
        ("pydantic", "Data validation library"),
        ("pytest", "Testing framework"),
        ("hypothesis", "Property-based testing"),
        ("python-multipart", "Multipart form support")
    ]
    
    failed_packages = []
    
    for package, description in dependencies:
        print(f"\n📦 Installing {package} ({description})...")
        if not run_command(f"python -m pip install {package}", f"Installing {package}"):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Some packages failed to install: {', '.join(failed_packages)}")
        print("🔧 Trying alternative installation methods...")
        
        # Try installing with --no-deps for problematic packages
        for package in failed_packages:
            print(f"🔄 Retrying {package} with --no-deps...")
            run_command(f"python -m pip install --no-deps {package}", f"Installing {package} without dependencies")
    
    print("\n✅ Installation process completed!")
    return len(failed_packages) == 0

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        import fastapi
        import uvicorn
        import numpy
        import pydantic
        print("✅ All core dependencies imported successfully!")
        
        # Test basic functionality
        print("🔬 Testing basic functionality...")
        
        # Test NumPy
        arr = numpy.array([1, 2, 3, 4])
        assert len(arr) == 4
        print("✅ NumPy working correctly")
        
        # Test FastAPI
        from fastapi import FastAPI
        app = FastAPI()
        print("✅ FastAPI working correctly")
        
        print("🎉 Installation test passed! The simulator should work correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Some dependencies may not be installed correctly.")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main installation process"""
    print("=" * 60)
    print("🎯 GPU Parallel Floating-Point Simulator Installation")
    print("📚 Educational tool for parallel programming concepts")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install dependencies
    success = install_dependencies()
    
    # Test installation
    if success:
        test_success = test_installation()
        
        if test_success:
            print("\n" + "=" * 60)
            print("🎉 Installation completed successfully!")
            print("\n🚀 To run the simulator:")
            print("1. python run_server.py")
            print("2. Open http://localhost:8000 in your browser")
            print("\n📖 For more information, see README.md")
            print("=" * 60)
        else:
            print("\n⚠️  Installation completed but tests failed.")
            print("The simulator may still work, but some features might be limited.")
    else:
        print("\n❌ Installation had some issues.")
        print("You may need to install dependencies manually:")
        print("pip install fastapi uvicorn numpy pydantic")

if __name__ == "__main__":
    main()