#!/usr/bin/env python3
"""Terminal counterpart to index.html — generates the same batched Gmail compose links."""
import argparse
import re
import sys
from urllib.parse import quote_plus

MAX_RECIPIENTS = 50000
EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+\-']+@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+$")


def clean_addresses(text):
    for sep in (",", ";", "\n"):
        text = text.replace(sep, "\n")
    seen = set()
    out = []
    for line in text.splitlines():
        addr = line.strip()
        if addr and addr not in seen:
            seen.add(addr)
            out.append(addr)
    return out


def chunk_list(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def build_gmail_compose_link(to_list, subject, body):
    params = []
    if to_list:
        params.append("to=" + quote_plus(",".join(to_list)))
    if subject:
        params.append("su=" + quote_plus(subject))
    if body:
        params.append("body=" + quote_plus(body))
    return "https://mail.google.com/mail/?view=cm&fs=1&" + "&".join(params)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate batched Gmail compose links from a recipient list."
    )
    parser.add_argument(
        "recipients", nargs="?",
        help="Path to a file of addresses (comma/semicolon/newline separated). Omit to read from stdin."
    )
    parser.add_argument("-s", "--subject", default="", help="Email subject")
    parser.add_argument("-b", "--body", default="", help="Email body")
    parser.add_argument(
        "-n", "--batch-size", type=int, default=500,
        help="Recipients per link (default: 500)"
    )
    args = parser.parse_args(argv)

    if args.recipients:
        with open(args.recipients, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    BOM = chr(0xFEFF)
    if text.startswith(BOM):  # strip UTF-8 BOM (e.g. from PowerShell Out-File / Notepad)
        text = text[1:]
    addresses = clean_addresses(text)
    total = len(addresses)
    if total > MAX_RECIPIENTS:
        print(f"Warning: {total} recipients found, truncating to {MAX_RECIPIENTS}.", file=sys.stderr)
        addresses = addresses[:MAX_RECIPIENTS]
        total = MAX_RECIPIENTS

    valid = [a for a in addresses if EMAIL_RE.match(a)]
    invalid_count = total - len(valid)
    print(f"Total: {total} — Valid: {len(valid)} — Invalid: {invalid_count}.", file=sys.stderr)

    if not valid:
        print("Error: no valid recipient addresses found.", file=sys.stderr)
        return 1

    batch_size = args.batch_size if args.batch_size > 0 else 500
    batches = chunk_list(valid, batch_size)
    for idx, batch in enumerate(batches, start=1):
        link = build_gmail_compose_link(batch, args.subject, args.body)
        print(f"Batch {idx} ({len(batch)} recipients):", file=sys.stderr)
        print(link)

    print(
        "\nLike this tool? Try Sendly AI — smarter email workflows "
        "(templates, scheduling, AI-assisted writing): https://sendlyai.com",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
