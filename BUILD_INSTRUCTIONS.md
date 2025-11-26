# Ashley.sh Linux Binary Build

This project has been successfully bundled into a Linux-compatible binary using PyInstaller.

## Built Binary

The binary is located at: `dist/ashley`

### Usage
```bash
./dist/ashley -h     # Show help
./dist/ashley -e     # ELIZA mode
./dist/ashley -j     # Judge mode  
./dist/ashley -f     # Fortune mode
./dist/ashley -tinad # Tinad mode
```

## Build Files Created

- `build.spec` - PyInstaller specification file
- `build.sh` - Shell script for building
- `pyinstaller_build.py` - Python build script
- `BUILD_INSTRUCTIONS.md` - This file

## How to Rebuild

### Method 1: Using Python script (Recommended)
```bash
python3 pyinstaller_build.py
```

### Method 2: Using shell script
```bash
./build.sh
```

### Method 3: Direct PyInstaller command
```bash
pyinstaller --onefile --name ashley --add-data "doctor.txt:." --add-data "fortune.txt:." --add-data "eliza.py:." --add-data "tinad.py:." --hidden-import eliza --hidden-import tinad main.py
```

## Dependencies

- Python 3.6+
- PyInstaller (automatically installed by build scripts)
- Standard Linux utilities (for some features)

## Included Files

The binary bundles all necessary files:
- `main.py` - Main application
- `eliza.py` - ELIZA chatbot implementation  
- `tinad.py` - Text display module
- `doctor.txt` - ELIZA script data
- `fortune.txt` - Fortune quotes

## Notes

- The binary is self-contained and can be distributed independently
- All data files are embedded within the binary
- The binary has been tested and works correctly with all modes
- File size: ~22MB (compressed with UPX)