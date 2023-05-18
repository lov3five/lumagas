from flask import Flask, render_template, request, redirect, url_for, flash, send_file

app = Flask(__name__)


# TEST
@app.route('/test')
def test():
    return "Hello World"

# GET Homepage
@app.route('/')
def index():
    return render_template('index.html')

