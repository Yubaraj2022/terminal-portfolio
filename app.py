import os
import re
from flask import Flask, render_template, abort
import mistune

app = Flask(__name__)

SCRIBBLES_DIR = os.path.join(os.path.dirname(__file__), "scribbles")
os.makedirs(SCRIBBLES_DIR, exist_ok=True)
SLUG_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def load_post(slug):
    if not SLUG_RE.fullmatch(slug):
        return None
    path = os.path.join(SCRIBBLES_DIR, f"{slug}.md")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    title = slug.replace("-", " ").title()
    body_lines = lines
    if lines and re.match(r"^#\s+", lines[0]):
        title = re.sub(r"^#\s+", "", lines[0]).strip()
        body_lines = lines[1:]

    return title, mistune.html("\n".join(body_lines).lstrip())


@app.route("/")
def manual():
    return render_template("manual.html", active_tab="manual", cmd="man yubaraj")


@app.route("/writing")
def writing():
    slugs = sorted(
        os.path.splitext(name)[0]
        for name in os.listdir(SCRIBBLES_DIR)
        if name.endswith(".md") and os.path.isfile(os.path.join(SCRIBBLES_DIR, name))
    )
    posts = []
    for slug in slugs:
        loaded = load_post(slug)
        if loaded:
            posts.append({"slug": slug, "title": loaded[0]})
    return render_template("writing.html", active_tab="writing", cmd="ls scribbles/", posts=posts)


@app.route("/writing/<slug>")
def post(slug):
    loaded = load_post(slug)
    if not loaded:
        abort(404)
    title, html = loaded
    return render_template(
        "post.html",
        active_tab="writing",
        cmd=f"cat scribbles/{slug}.md",
        title=title,
        content=html,
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
