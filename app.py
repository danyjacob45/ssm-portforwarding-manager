from datetime import datetime
from flask import Flask, render_template, make_response, request, redirect, url_for
import config
import ssm
from model import db, SSMAgentList

app = config.create_app()

@app.route('/')
def startup():
    return listDetails()


@app.route('/list', methods=['GET'])
def listDetails():
    try:
        response = ssm.setup()
        #response = ssm.setupDummy()
        try:
            for each in response:
                record = SSMAgentList.query.filter_by(instance_id = each['instance_id']).first()
                if(record):
                    continue
                ssm_Obj = SSMAgentList(profile=each['profile'],
                                       instance_id=each['instance_id'],
                                       platform=each['platform'],
                                       tag_name=each['tag_name'],
                                       connect_port="not connected",
                                       updated_time=datetime.now()
                                       )
                db.session.add(ssm_Obj)
                db.session.commit()
        except:
            pass
    except:
        return make_response("Something went wrong! Try again!")
    column_names = ['profile', 'instance_id', 'platform', 'tag_name', 'connect_port']
    return render_template('record.html', records=response, colnames=column_names)


@app.route('/update', methods=['GET'])
def update():
    try:
        id = request.args['id']
        port = request.args['connect_port']
        #query from db now...
        record = SSMAgentList.query.filter_by(instance_id=id).first()
        record.connect_port = port
        record.updated_time = datetime.now()
        db.session.add(record)
        db.session.commit()
        response = []
        for each in SSMAgentList.query.all():
            response.append(each.to_json())
    except Exception as e:
        print(e)
        return make_response("Something went wrong! Try again!")
    column_names = ['profile', 'instance_id', 'platform', 'tag_name', 'connect_port']
    return render_template('record.html', records=response, colnames=column_names)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    print("connect pressed")
    id = request.args['instance_id']
    platform = request.args['platform']
    profile = request.args['profile']
    try:
        execution_result = ssm.executeSSM(id, platform, profile)
        #execution_result = '1000'
    except:
        return make_response("Something went wrong! Try again!")
    return redirect(url_for('update', connect_port=execution_result, id=id))
    # return "The tunnel to server "+id +" is open on port " + str(execution_result)+ ". Press back to go back to previous page.."


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    print("disconnect pressed")


if __name__ == '__main__':
    app.run(debug=True)
