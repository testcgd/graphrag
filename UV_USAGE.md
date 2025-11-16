# Using UV with GraphRAG

[uv](https://github.com/astral-sh/uv) is a modern, fast Python package manager written in Rust. It can be used as a faster alternative to Poetry for installing and managing dependencies in the GraphRAG project.

## Why Use UV?

- **Speed**: 10-100x faster than pip and significantly faster than Poetry
- **Compatibility**: Works with existing `pyproject.toml` files
- **Reliability**: Deterministic dependency resolution
- **Modern**: Built with modern Python packaging standards (PEP 621, PEP 660)

## Installation

### Linux / macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Using pip
```bash
pip install uv
```

## Quick Start

### Installing GraphRAG Dependencies

```bash
# Install production dependencies
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"
```

### Creating a Virtual Environment

```bash
# Create a new virtual environment
uv venv

# Activate it
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Running GraphRAG Commands

```bash
# Using uv run (creates isolated environment automatically)
uv run graphrag index --root ./ragtest
uv run graphrag query --root ./ragtest --method local "Your question"

# Or activate the environment first
source .venv/bin/activate
graphrag index --root ./ragtest
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_example.py

# Run with coverage
uv run pytest --cov=graphrag tests/
```

## Common Workflows

### Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/microsoft/graphrag.git
cd graphrag

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS

# 4. Install dependencies
uv pip install -e ".[dev]"

# 5. Verify installation
graphrag --version
```

### Update Dependencies

```bash
# Sync dependencies from pyproject.toml
uv pip sync requirements.txt

# Or update specific package
uv pip install --upgrade package-name
```

### Adding New Dependencies

Since this project uses Poetry for dependency management, add dependencies through Poetry:

```bash
# Add a new dependency
poetry add package-name

# Then sync with uv
uv pip install -e ".[dev]"
```

## UV vs Poetry

| Feature | UV | Poetry |
|---------|-----|--------|
| Install Speed | ★★★★★ (Very Fast) | ★★★☆☆ (Moderate) |
| Resolution Speed | ★★★★★ (Very Fast) | ★★★☆☆ (Moderate) |
| Lock File | uv.lock (optional) | poetry.lock |
| Dependency Management | Via pip interface | Built-in |
| Build System | Uses Poetry backend | Native |
| Python Version Management | Built-in | Via pyenv/asdf |

## Using UV with Poetry (Hybrid Approach)

You can use UV for faster installations while keeping Poetry for dependency management:

```bash
# Use Poetry to manage dependencies
poetry add new-package

# Use UV for faster installation
uv pip install -e ".[dev]"
```

## Configuration

UV configuration is defined in `pyproject.toml` under `[tool.uv]`:

```toml
[tool.uv]
python-version = ">=3.10,<3.13"
cache-dir = ".uv-cache"

[tool.uv.pip]
prerelease = "if-necessary"
resolution = "highest"
compile-bytecode = true
```

## Tips and Best Practices

### 1. Use Virtual Environments

Always use virtual environments to isolate project dependencies:

```bash
uv venv
source .venv/bin/activate
```

### 2. Cache Management

UV caches packages for faster reinstallation:

```bash
# View cache statistics
uv cache dir

# Clean cache
uv cache clean
```

### 3. Reproducible Installations

For reproducible installations, use requirements files:

```bash
# Export current environment
uv pip freeze > requirements.txt

# Install from requirements
uv pip install -r requirements.txt
```

### 4. Parallel Installation

UV installs packages in parallel by default for maximum speed. No configuration needed!

### 5. Offline Mode

UV can work offline if packages are cached:

```bash
uv pip install --no-network package-name
```

## Troubleshooting

### Issue: "No such file or directory: 'uv'"

**Solution**: Make sure UV is installed and in your PATH:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your shell or run:
source $HOME/.cargo/env
```

### Issue: Dependency conflicts

**Solution**: UV uses strict dependency resolution. Check `pyproject.toml` for conflicts:
```bash
uv pip install -e . --verbose
```

### Issue: Slow first installation

**Solution**: First installation builds cache. Subsequent installs will be much faster:
```bash
# First time (builds cache)
uv pip install -e ".[dev]"  # May take a few minutes

# Subsequent times (uses cache)
uv pip install -e ".[dev]"  # Very fast!
```

## Migrating from Poetry to UV (Optional)

If you want to fully migrate from Poetry to UV:

### 1. Export Poetry dependencies
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### 2. Create UV lock file
```bash
uv pip compile requirements.txt -o uv.lock
```

### 3. Install from lock file
```bash
uv pip sync uv.lock
```

**Note**: This project currently uses Poetry as the primary dependency manager. UV is provided as an optional faster installer.

## CI/CD Integration

UV is great for CI/CD pipelines due to its speed:

```yaml
# GitHub Actions example
- name: Install dependencies
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv pip install -e ".[dev]"
```

## Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV Installation Guide](https://astral.sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)
- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)

## Questions?

- For UV-specific issues: [UV GitHub Issues](https://github.com/astral-sh/uv/issues)
- For GraphRAG issues: [GraphRAG GitHub Issues](https://github.com/microsoft/graphrag/issues)
