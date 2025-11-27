# Ashley.sh

A Linux binary application built with PyInstaller.

## Release Process

To create a new release:

### 1. Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. GitHub Actions will automatically:
- Build the binary using the exact PyInstaller command from BUILD_INSTRUCTIONS.md
- Create a GitHub release with the built binary attached
- Generate release notes automatically

### 3. The release will be available at:
`https://github.com/[username]/[repository]/releases`

## Build Command Used

The GitHub Actions workflow uses the exact PyInstaller command from the build instructions:
```bash
pyinstaller --onefile --name ashley --add-data "doctor.txt:." --add-data "fortune.txt:." --add-data "eliza.py:." --add-data "tinad.py:." --hidden-import eliza --hidden-import tinad main.py
```

## Usage

Download the binary from the latest release and run:
```bash
./ashley -h     # Show help
./ashley -e     # ELIZA mode
./ashley -j     # Judge mode  
./ashley -f     # Fortune mode
./ashley -tinad # Tinad mode
```