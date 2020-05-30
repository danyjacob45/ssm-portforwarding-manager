from flask import Flask, render_template, make_response, jsonify, request
import requests
import ssm

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/test', methods=['GET'])
def jsonparser():
    # url = "https://jsonplaceholder.typicode.com/todos/"
    # response = requests.get(url)
    # json_dict = response.json()
    response = ssm.setup()
    column_names = ['profile', 'instance_id', 'platform', 'tag_tame']
    return render_template('record.html', records=response, colnames=column_names)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    print("connect pressed")
    port = request.args['port']
    id = request.args['instance_id']
    platform = request.args['platform']
    profile = request.args['profile']
    # ssm.executeSSM(id,platform,profile,port)
    return "Hello from port# " + port


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    print("disconnect pressed")


if __name__ == '__main__':
    app.run()
