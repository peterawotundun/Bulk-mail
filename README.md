# Bulk-mail

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[Contributors ➜](CONTRIBUTORS.md)

A professional single-file Bulk Gmail Link Generator intended for manual workflows.

Features
- Open `index.html` directly in a browser (no server required).
- Upload a CSV (one email per line) or paste recipient emails.
- Validates and deduplicates addresses client-side and splits recipients into batches (default 500).
- Generates Gmail compose links with all recipients in the To field.
- Copy individual links, copy all links, or download a ZIP containing one HTML per batch.

Usage
1. Clone or download the repository.
2. Open `index.html` in your browser.
3. Upload/paste recipients, enter subject and body, and click "Generate links".

Behavior
- All recipients are placed in the To field; batch size is configurable and defaults to 500.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
