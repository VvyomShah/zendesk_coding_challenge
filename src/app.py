from flask import Flask
import urllib.request
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "<p> Hello World </p>"

def getToken():
    pass

def getTicket():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8080)