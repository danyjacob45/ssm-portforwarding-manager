from flask import Flask, render_template, make_response, jsonify, request, redirect, url_for
import requests
import ssm

app = Flask(__name__)


@app.route('/')
def hello_world():
    return listDetails()


@app.route('/list', methods=['GET'])
def listDetails():
    try:
        response = ssm.setup()
    except:
        return make_response("Something went wrong! Try again!")
    column_names = ['profile', 'instance_id', 'platform', 'tag_tame', 'free_port']
    return render_template('record.html', records=response, colnames=column_names)


@app.route('/update', methods=['GET'])
def update():
    response = ssm.setup()
    column_names = ['profile', 'instance_id', 'platform', 'tag_tame', 'free_port']
    return render_template('record.html', records=response, colnames=column_names)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    print("connect pressed")
    id = request.args['instance_id']
    platform = request.args['platform']
    profile = request.args['profile']
    try:
        execution_result = ssm.executeSSM(id, platform, profile)
    except:
        return make_response("Something went wrong! Try again!")
    return redirect(url_for('update', free_port=execution_result, id=id))
    # return "The tunnel to server "+id +" is open on port " + str(execution_result)+ ". Press back to go back to previous page.."


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    print("disconnect pressed")


if __name__ == '__main__':
    app.run()
