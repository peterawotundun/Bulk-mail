from flask import Flask, render_template, request
from urllib.parse import quote_plus
import math

app = Flask(__name__)

def clean_addresses(text):
    # split on commas, semicolons, or newlines and strip whitespace
    parts = []
    for sep in [",", ";", "\n"]:
        text = text.replace(sep, "\n")
    for line in text.splitlines():
        addr = line.strip()
        if addr:
            parts.append(addr)
    # deduplicate while preserving order
    seen = set()
    out = []
    for a in parts:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def build_gmail_compose_link(to_list, subject, body):
    # Gmail compose URL:
    # https://mail.google.com/mail/?view=cm&fs=1&to=...&su=...&body=...&bcc=...
    # We'll put the first recipient in "to" and the rest in "bcc" to avoid very long "to" fields.
    to_field = ""
    bcc_field = ""
    if len(to_list) == 0:
        to_field = ""
    elif len(to_list) == 1:
        to_field = to_list[0]
    else:
        to_field = to_list[0]
        bcc_field = ",".join(to_list[1:])
    params = []
    if to_field:
        params.append("to=" + quote_plus(to_field))
    if subject:
        params.append("su=" + quote_plus(subject))
    if body:
        params.append("body=" + quote_plus(body))
    if bcc_field:
        params.append("bcc=" + quote_plus(bcc_field))
    return "https://mail.google.com/mail/?view=cm&fs=1&" + "&".join(params)

@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")

@app.route("/generate", methods=["POST"])
def generate():
    sender = request.form.get("sender", "").strip()
    subject = request.form.get("subject", "").strip()
    title = request.form.get("title", "").strip()  # optional UI title only
    body = request.form.get("body", "").strip()
    receivers = request.form.get("receivers", "").strip()
    try:
        batch_size = int(request.form.get("batch_size", "100"))
        if batch_size <= 0:
            batch_size = 100
    except ValueError:
        batch_size = 100

    recipients = clean_addresses(receivers)
    total = len(recipients)
    if total == 0:
        return "No recipient addresses provided.", 400
    if total > 50000:
        return "Too many recipients. Limit is 50,000.", 400

    batches = list(chunk_list(recipients, batch_size))
    links = []
    for idx, batch in enumerate(batches, start=1):
        link = build_gmail_compose_link(batch, subject, body)
        links.append({
            "batch_number": idx,
            "count": len(batch),
            "link": link,
            "preview_to": batch[0] if batch else ""
        })

    return render_template("results.html", sender=sender, subject=subject, title=title,
                           total=total, batch_size=batch_size, links=links)

if __name__ == "__main__":
    app.run(debug=True)