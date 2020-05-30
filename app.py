from flask import Flask, render_template, make_response, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/test', methods = ['GET'])
def jsonparser():
    url = "https://jsonplaceholder.typicode.com/todos/"
    response = requests.get(url)
    json_dict = response.json()
    column_names = ['userid','id','title','completed']
    return render_template('record.html', records=json_dict, colnames=column_names)

@app.route('/connect', methods = ['GET'])
def connect():
    print("connect pressed")

@app.route('/disconnect', methods = ['GET'])
def disconnect():
    print("disconnect pressed")


if __name__ == '__main__':

    app.run()
