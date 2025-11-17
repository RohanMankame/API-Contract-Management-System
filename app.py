from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return "index page"



if __name__ == '__main__':
    app.run(debug=True)