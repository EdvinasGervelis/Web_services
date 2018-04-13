from flask import Flask
from flask import request
from flask import jsonify
from flask import abort

import os
import re

app = Flask(__name__)

visits = [
          {'ID': '1',  'AK':'49612033268', 'Name' : 'Lina', 'Surname' : 'Kudirkaite', 'Date' : 'Kovo 21 d', 'Time': '11.30'},
          {'ID': '2', 'AK':'49608052145', 'Name' : 'Kristina', 'Surname' : 'Kateraite', 'Date' : 'Kovo 19 d', 'Time' : '10.15'}
          ]

@app.route('/')
def hello():
    return'Patients visits schedules'

@app.route('/visits/schedules', methods=['GET'])
def get_all_info():
    if( request.args.get('Name', '')):
        findPatients = []
        for i in visits:
            if( re.search(request.args.get('Name', ''), i["Name"], re.IGNORECASE)):
                findPatients.append(i)
        return jsonify(findPatients)
    else:
        return jsonify(visits), 200

@app.route('/visits/schedules/<patAK>', methods=['DELETE'])
def delete_pat(patAK):
    deleted_pat=[pat for pat in visits if (pat['ID'] == patAK)]
    if len(deleted_pat) == 0:
        abort(404)
    visits.remove(deleted_pat[0])
    return jsonify(True), 200
@app.route('/visits/schedules', methods=['POST'])
def new_appointment():
    if not request.json or not 'AK' in request.json:
        abort(404)
    if not 'Date' or not 'Name' in request.json:
        abort(404)
    if not 'Time' or not 'Surname' in request.json:
        abort(404)
    lastId = int(visits[len(visits) - 1]['ID']) + 1
    new_app={
        'ID' :  str(lastId),
        'AK' : request.json['AK'],
        'Name' : request.json['Name'],
        'Surname' : request.json['Surname'],
        'Date' : request.json['Date'],
        'Time' : request.json['Time']
        }
    visits.append(new_app)
    return jsonify(new_app),201,{'Location': '/visits/schedules/'+str(visits[-1]['ID'])}
@app.route('/visits/schedules/<switchAK>',methods=['PUT'])
def updateVisits(switchAK):
    up = [ upd for upd in visits if (upd['ID'] == switchAK)]
    if 'Date' in request.json:
        up[0]['Date'] = request.json['Date']
    if 'Time' in request.json:
        up[0]['Time'] = request.json['Time']
    return jsonify(up[0]), 200

@app.route('/visits/schedules/<patieninf>', methods=['GET'])
def getPatient(patieninf):
    pat = [ pak for pak in visits if (pak['ID'] == patieninf
            or pak['Name'] == patieninf or pak['Surname'] == patieninf
            or pak ['Date'] == patieninf or pak['Time'] == patieninf)]
    if len(pat) == 0:
        abort(404)
    return jsonify(pat)

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")
    

