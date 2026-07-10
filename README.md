# Bulk-mail

This repository contains a tiny Bulk Gmail Link Generator. Two modes are available:

- The original Flask-based app (app.py + templates/) which requires running a Python Flask server.
- A standalone frontend: `index.html` — a single-file, client-side app that you can open directly in your browser (double-click the file) without running a server.

What the standalone `index.html` does
- Accepts a CSV file (single-column: one email per line) or pasted emails (one per line).
- Validates email addresses with a practical client-side regex and deduplicates them.
- Splits recipients into batches (configurable batch size, default 500).
- Generates Gmail compose links for each batch (first recipient in To, rest in BCC).
- Lets you copy links, copy all links, or download a ZIP containing one HTML file per batch with a button to open the composer.

How to use `index.html` (no terminal required)
1. Clone the repo or download the files.
2. Double-click `index.html` to open it in your browser (or open it via File -> Open).
3. Paste or upload your recipients (CSV single-column). Enter subject and body, set batch size (default 500), click "Generate links".
4. Click a link to open the Gmail composer with fields pre-filled, then click Send.

Notes and limitations
- Sender address cannot be forced by the Gmail compose URL. Because the app opens Gmail's composer directly in the user's browser, Gmail will automatically use the currently-signed-in account as the sender; users should verify the From address inside Gmail if they have multiple accounts.
- URL-length, browser, and Gmail limits exist. Packing thousands of addresses into a single URL can fail; that’s why batching is used. The app enforces a 50,000 recipient cap but you should use conservative batch sizes (default 500).
- The client-side app uses a practical JavaScript email regex for validation. The Python `email-validator` package is not used because this is a browser-only implementation. If you prefer server-side validation with `email-validator`, run the Flask app and I can integrate it there.

If you want me to remove the Flask app and replace it with a serverless design or to add server-side email-validator support, tell me and I will update the repository accordingly.
