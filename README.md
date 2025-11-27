# Ashley.sh

a linux binary that puts ashley in your puper


## Release Process

to create a new release:

### 1. Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. GitHub Actions will automatically do the thing

## Usage

Download the binary from the latest release and run:
```bash
./ashley -h     # Show help
./ashley -e     # ELIZA mode
./ashley -j     # Judge mode  
./ashley -f     # Fortune mode
./ashley -tinad # Tinad mode
```
