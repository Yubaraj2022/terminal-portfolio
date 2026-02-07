from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html', active_tab="welcome")

@app.route('/projects')
def projects():
    # You can pass your list of projects here later!
    return render_template('index.html', active_tab="projects")

@app.route('/scribble')
def scribble():
    return render_template('index.html', active_tab="scribble")

@app.route('/contact')
def contact():
    return render_template('index.html', active_tab="contact")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)