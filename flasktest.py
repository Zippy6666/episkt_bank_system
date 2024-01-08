import webbrowser
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return "amogus gaming" # render_template('debank.html')


# Launch the web browser before running the app
webbrowser.open("http://127.0.0.1:5000/")


# Run the app with the specified host and port
app.run("127.0.0.1", port=5000)