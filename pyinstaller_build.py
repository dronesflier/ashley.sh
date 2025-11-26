#!/usr/bin/env python3
"""
PyInstaller build script for Ashley.sh
This script can be run directly to build the Linux binary.
"""

import os
import subprocess
import sys

def build_binary():
    """Build the Ashley.sh binary using PyInstaller"""
    
    print("Building Ashley.sh Linux binary...")
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller is not installed.")
        print("Please install it with: pip install pyinstaller")
        return False
    
    # Clean previous builds
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "ashley",
        "--add-data", "doctor.txt:.",
        "--add-data", "fortune.txt:.",
        "--add-data", "eliza.py:.",
        "--add-data", "tinad.py:.",
        "--hidden-import", "eliza",
        "--hidden-import", "tinad",
        "main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Build successful!")
            print(f"Binary created at: dist/ashley")
            
            # Test if the binary works
            if os.path.exists("dist/ashley"):
                print("\nTesting binary...")
                test_result = subprocess.run(["dist/ashley", "-h"], capture_output=True, text=True)
                if test_result.returncode == 0:
                    print("✓ Binary test passed!")
                else:
                    print("⚠ Binary test failed, but build completed.")
                    print(f"Error output: {test_result.stderr}")
            
            print("\nUsage:")
            print("  ./dist/ashley -h     # Show help")
            print("  ./dist/ashley -e     # ELIZA mode")
            print("  ./dist/ashley -j     # Judge mode")
            print("  ./dist/ashley -f     # Fortune mode")
            print("  ./dist/ashley -tinad # Tinad mode")
            
            return True
        else:
            print("Build failed!")
            print(f"Error: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"Build failed with exception: {e}")
        return False

if __name__ == "__main__":
    build_binary()