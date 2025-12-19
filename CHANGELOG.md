# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-19

### Added
- Initial release
- Flask HTTP server with REST API
- Advanced image preprocessing pipeline
  - CLAHE contrast enhancement
  - Adaptive thresholding
  - Morphological operations
  - Image scaling (2x)
- Multiple Tesseract OCR configurations (PSM 6, 7, 8)
- Voting mechanism for improved accuracy
- Health check endpoint (`GET /health`)
- API documentation endpoint (`GET /`)
- Support for base64 and data URL image formats
- Docker and Docker Compose support
