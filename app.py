from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return "index page"

@app.route('/createContract', methods=['POST'])
def createContract():
    pass 

@app.route('/deleteContract', methods=['DELETE'])
def deleteContractByID():
    pass 

@app.route('/getContract', methods=['GET'])
def getContractByID():
    pass 

def getContractByClient():
    pass



if __name__ == '__main__':
    app.run(debug=True)