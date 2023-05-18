from flask import Flask, render_template, jsonify

from app.routes import *

app = Flask(__name__)

# TEST
@app.route('/api/test', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, world!'})

# GET homepage LUMAGAS
@app.route('/')
def index():
    return render_template('index.html')




