#!/bin/bash

# Build script for Ashley.sh Linux binary

echo "Building Ashley.sh Linux binary..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller is not installed. Please install it with:"
    echo "pip install pyinstaller"
    exit 1
fi

# Clean previous builds
rm -rf build/ dist/

# Build using the spec file
pyinstaller build.spec

# Check if build was successful
if [ -f "dist/ashley" ]; then
    echo "Build successful!"
    echo "Binary created at: dist/ashley"
    echo ""
    echo "Usage:"
    echo "  ./dist/ashley -h     # Show help"
    echo "  ./dist/ashley -e     # ELIZA mode"
    echo "  ./dist/ashley -j     # Judge mode"
    echo "  ./dist/ashley -f     # Fortune mode"
    echo "  ./dist/ashley -tinad # Tinad mode"
else
    echo "Build failed!"
    exit 1
fi