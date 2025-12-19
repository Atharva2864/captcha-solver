# Captcha Solver 🔓

A free, lightweight, self-hosted CAPTCHA solver using **Tesseract OCR** with advanced image preprocessing. Run it locally and solve CAPTCHAs via a simple HTTP API — no external services, no API keys, no costs.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

## ✨ Features

- 🚀 **Simple HTTP API** — Send base64 image, get solved text
- 🔧 **Advanced Preprocessing** — CLAHE, adaptive thresholding, morphological operations
- 🎯 **Multi-strategy OCR** — Multiple Tesseract configurations for better accuracy
- 📊 **Voting Mechanism** — Returns most common result across strategies
- 💰 **100% Free** — No API keys, no subscriptions, runs entirely on your machine
- ⚡ **Lightweight** — Minimal dependencies, fast startup
- 🐳 **Docker Ready** — One command to run with Docker

## 📋 Requirements

- Python 3.8+
- Tesseract OCR installed on your system

## 🚀 Quick Start

### 1. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from [Tesseract GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)

### 2. Clone & Install

```bash
# Clone the repository
git clone https://github.com/Atharva2864/captcha-solver.git
cd captcha-solver

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python solver_server.py
```

You should see:
```
    ╔═══════════════════════════════════════════════════════╗
    ║           Captcha Solver Server v1.0.0                ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Server running at: http://127.0.0.1:5555             ║
    ╚═══════════════════════════════════════════════════════╝
```

## 🐳 Docker

```bash
# Build and run
docker-compose up -d

# Or build manually
docker build -t captcha-solver .
docker run -p 5555:5555 captcha-solver
```

## 📖 API Reference

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "captcha-solver",
  "version": "1.0.0"
}
```

### Solve CAPTCHA

```http
POST /solve
Content-Type: application/json

{
  "image": "<base64_encoded_image>"
}
```

**Success Response:**
```json
{
  "success": true,
  "text": "Ab3XyZ"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Could not solve CAPTCHA"
}
```

## 💻 Usage Examples

### cURL

```bash
# Health check
curl http://localhost:5555/health

# Solve CAPTCHA from file
curl -X POST http://localhost:5555/solve \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$(base64 -i captcha.png)\"}"
```

### Python

```python
import requests
import base64

# Read image and encode to base64
with open("captcha.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# Send to solver
response = requests.post(
    "http://localhost:5555/solve",
    json={"image": image_base64}
)

result = response.json()
if result["success"]:
    print(f"Solved: {result['text']}")
else:
    print(f"Failed: {result['error']}")
```

### JavaScript / Node.js

```javascript
const fs = require('fs');

// Read image and encode to base64
const imageBase64 = fs.readFileSync('captcha.png').toString('base64');

// Send to solver
const response = await fetch('http://localhost:5555/solve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageBase64 })
});

const result = await response.json();
console.log(result.success ? `Solved: ${result.text}` : `Failed: ${result.error}`);
```

### JavaScript (Browser)

```javascript
// Get image from canvas
const canvas = document.createElement('canvas');
const img = document.querySelector('img.captcha');
canvas.width = img.width;
canvas.height = img.height;
canvas.getContext('2d').drawImage(img, 0, 0);
const base64Image = canvas.toDataURL('image/png');

// Send to solver (works with data URL format too!)
const response = await fetch('http://localhost:5555/solve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: base64Image })
});

const result = await response.json();
```

### C# / .NET

```csharp
using var httpClient = new HttpClient();

// Read and encode image
var imageBytes = await File.ReadAllBytesAsync("captcha.png");
var base64Image = Convert.ToBase64String(imageBytes);

// Send to solver
var payload = JsonSerializer.Serialize(new { image = base64Image });
var content = new StringContent(payload, Encoding.UTF8, "application/json");
var response = await httpClient.PostAsync("http://localhost:5555/solve", content);

var result = await response.Content.ReadAsStringAsync();
Console.WriteLine(result);
```

## 🏗️ How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  CAPTCHA Image  │────▶│   Preprocessing  │────▶│  Tesseract OCR  │
│   (Base64)      │     │  • Grayscale     │     │  • PSM 7        │
└─────────────────┘     │  • CLAHE         │     │  • PSM 8        │
                        │  • Threshold     │     │  • PSM 6        │
                        │  • Morphology    │     └────────┬────────┘
                        │  • Scale 2x      │              │
                        └──────────────────┘              ▼
                                              ┌─────────────────────┐
                                              │   Voting/Selection  │
                                              │  (Most common text) │
                                              └──────────┬──────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────────┐
                                              │   JSON Response     │
                                              │  {"text": "Ab3XyZ"} │
                                              └─────────────────────┘
```

### Preprocessing Pipeline

1. **Grayscale Conversion** — Simplify the image to single channel
2. **CLAHE** — Enhance contrast while limiting noise amplification
3. **Adaptive Thresholding** — Convert to binary image, handles varying backgrounds
4. **Morphological Operations** — Remove noise and connect broken characters
5. **Scaling** — Upscale 2x for better OCR accuracy

### Multi-Strategy OCR

The solver tries multiple Tesseract Page Segmentation Modes (PSM):
- **PSM 6** — Assume a uniform block of text
- **PSM 7** — Treat the image as a single text line
- **PSM 8** — Treat the image as a single word

Results are collected and the most common answer is returned (voting mechanism).

## ⚙️ Configuration

You can modify these settings in `solver_server.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `HOST` | `127.0.0.1` | Server host |
| `PORT` | `5555` | Server port |
| `MIN_LENGTH` | `4` | Minimum valid CAPTCHA length |

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- 🔧 Improve OCR accuracy with better preprocessing
- 🧪 Add unit tests
- 📊 Add confidence scores
- 🔌 Support for different CAPTCHA types
- 🌐 Web UI for testing

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided for **educational and legitimate automation purposes only**. Users are responsible for ensuring their use complies with applicable laws and terms of service. The authors are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — The OCR engine
- [OpenCV](https://opencv.org/) — Image processing library
- [Flask](https://flask.palletsprojects.com/) — Web framework

---

<p align="center">
  Made with ❤️ by Amey
</p>
