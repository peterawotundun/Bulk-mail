# Bulk-mail

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[Contributors ➜](CONTRIBUTORS.md)

A Bulk Gmail Link Generator, usable from your browser or your terminal. Also a small showcase for [Sendly AI](https://sendlyai.com), smarter email workflows.

## Architecture

Two independent, dependency-light entry points implement the same algorithm (clean → validate → dedupe → chunk → build Gmail compose links) with no server, database, or framework required for either:
- `index.html` — a zero-backend browser tool: vanilla JS, no build step, no install.
- `bulkmail.py` — a Python-stdlib-only CLI for terminal workflows: no `pip install` needed.

Features
- Upload a CSV (one email per line) or paste recipient emails.
- Validates and deduplicates addresses and splits recipients into batches (default 500).
- Generates Gmail compose links with all recipients in the To field.
- Copy individual links, copy all links, or download a ZIP containing one HTML per batch (browser only).

## Usage — Browser

1. Clone or download the repository.
2. Open `index.html` in your browser.
3. Upload/paste recipients, enter subject and body, and click "Generate links".

## Usage — Terminal

Requires Python 3 — nothing to install.

```
python bulkmail.py recipients.txt -s "Subject line" -b "Body text" -n 500
```

or pipe recipients in via stdin:

```
cat recipients.txt | python bulkmail.py -s "Subject line" -b "Body text"
```

Links print to stdout (one per line, ready to pipe or open); a summary and batch labels print to stderr.

Behavior
- All recipients are placed in the To field; batch size is configurable and defaults to 500.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
