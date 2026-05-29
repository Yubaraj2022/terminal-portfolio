import os
from flask import Flask, render_template, abort
import mistune

app = Flask(__name__)

# Locate the scribbles directory relative to this app.py file
SCRIBBLES_DIR = os.path.join(os.path.dirname(__file__), 'scribbles')

# Ensure the scribbles directory exists automatically
if not os.path.exists(SCRIBBLES_DIR):
    os.makedirs(SCRIBBLES_DIR)

@app.route('/')
def index():
    return render_template('welcome.html', active_tab="welcome")

@app.route('/projects')
def projects():
    return render_template('projects.html', active_tab="projects")

@app.route('/scribble')
def scribble():
    files = []
    if os.path.exists(SCRIBBLES_DIR):
        # Fetch clean file names without the .md extension to use in URLs
        files = [f.replace('.md', '') for f in os.listdir(SCRIBBLES_DIR) if f.endswith('.md')]
    return render_template('scribble.html', active_tab="my-scribbles", files=files)

@app.route('/scribble/<filename>')
def view_scribble(filename):
    safe_filename = f"{filename}.md"
    file_path = os.path.join(SCRIBBLES_DIR, safe_filename)
    
    # Standard 404 handler if someone types a non-existent file name in the URL
    if not os.path.exists(file_path):
        abort(404)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    # Render markdown text into clean HTML layout blocks
    html_content = mistune.html(markdown_content)
    
    return render_template('view_scribble.html', active_tab="my-scribbles", content=html_content, title=filename)

@app.route('/contact')
def contact():
    return render_template('contact.html', active_tab="contact-me")

if __name__ == '__main__':
    # Listens on port 5000 across your entire local area home network
    app.run(debug=True, host='0.0.0.0', port=5000)
