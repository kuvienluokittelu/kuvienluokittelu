from flask import Flask
from flask import send_file
from markupsafe import escape
from urllib.parse import urlparse
import urllib.request

# Vielä käyttämättömät, valmiiksi importoitu
from yolov5 import eval

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/imageval/<path:imageURL>', methods=['GET', 'POST'])
def image_evaluation(imageURL):

    filename = "evaluated_image.jpg"
    parsedUrl = urlparse(imageURL)

    urllib.request.urlretrieve(parsedUrl.geturl(), filename)

    return send_file(filename)
