from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_caching import Cache
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import logging
import validators
from scraping.scraper import scrape_website
from processing.summarizer import summarize_text

# Initialize Flask app
app = Flask(__name__)

# Configure secret key
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize cache
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set the login view

# User class
class User(UserMixin):
    pass

# User loader
@login_manager.user_loader
def user_loader(user_id):
    if user_id == '1':
        user = User()
        user.id = '1'
        return user
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            user = User()
            user.id = '1'
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Process summary
def process_summary(text):
    lines = text.splitlines()
    output = []
    in_ol = False
    in_ul = False
    in_p = False

    for line in lines:
        line = line.strip()
        if not line:
            if in_p:
                output.append("</p>")
                in_p = False
            output.append("<br>")
            continue

        if line.startswith("**") and line.endswith(":**"):
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if in_p:
                output.append("</p>")
                in_p = False
            header = line[2:-3]  # Remove "**" and ":**"
            output.append("<br><strong>{}</strong><br>".format(header))
        elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. "):
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            item = line[3:].strip()
            output.append("<li>{}</li>".format(item))
        elif line.startswith("- "):
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            item = line[2:].strip()
            output.append("<li>{}</li>".format(item))
        else:
            if not in_p:
                output.append("<p>")
                in_p = True
            output.append(line)

    # Close any open tags
    if in_ol:
        output.append("</ol>")
    if in_ul:
        output.append("</ul>")
    if in_p:
        output.append("</p>")

    # Join all elements into a single string
    processed_text = "\n".join(output)
    return processed_text

# Index route
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not validators.url(url):
            return render_template('index.html', error='Invalid URL format.')
        cached_summary = cache.get(url)
        if cached_summary:
            return render_template('result.html', summary=cached_summary)
        text = scrape_website(url)
        summary = str(summarize_text(text))
        processed_summary = process_summary(summary)
        cache.set(url, processed_summary, timeout=3600)
        return render_template('result.html', processed_summary=processed_summary)
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, filename='error.log', filemode='a',
                        format='%(name)s - %(levelname)s - %(message)s')
    app.run(debug=True)
