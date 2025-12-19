# Contributing to Captcha Solver

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Sample CAPTCHA image** (if possible)
- **Environment details** (OS, Python version, Tesseract version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear description** of the enhancement
- **Use case** explaining why this would be useful
- **Possible implementation** if you have ideas

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/captcha-solver.git
cd captcha-solver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python solver_server.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Ideas for Contribution

- 🔧 Improve OCR accuracy with better preprocessing
- 📊 Add confidence scores to responses
- 🧪 Add unit tests
- 📝 Improve documentation
- 🐳 Improve Docker setup
- 🔌 Add support for different CAPTCHA types
- 🌐 Create a simple web UI for testing
- ⚡ Performance optimizations

## Questions?

Feel free to open an issue for any questions!
