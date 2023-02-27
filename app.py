from flask import Flask, render_template, request
import os
import numpy as np
from main import Submit
from werkzeug.serving import ThreadedWSGIServer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get text input from the form
        text = request.form['text']

        # Create the video
        video_link = Submit(text)

        # Render the template with the video link
        return render_template('result.html', video_link=video_link)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # Use a threaded WSGI server for multiple threads
    http_server = ThreadedWSGIServer('', 5000, app)
    http_server.serve_forever()
