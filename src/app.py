#!flask/bin/python
from flask import Flask, abort
from flask import jsonify
from flask import make_response
from flask import request
import json


app = Flask(__name__)

def read_from_json():
    items = json.load(open('data.json'))
    return items

def write_to_json(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/items', methods=['GET'])
def get_items():
    items = read_from_json()
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = read_from_json()
    if ((item_id <= items['items'][-1]['id']) & (item_id >= items['items'][0]['id'])):
        item = [item for item in items['items'] if item['id'] == item_id]
        if len(item) == 0:
            not_found(404)
        return jsonify({'item': item[0]})
    else:
        return not_found(404)

@app.route('/items', methods=['POST'])
def create_item():
    items = read_from_json()
    if not request.json or not 'description' or not 'brand' or not 'model' or not 'quantity' in request.json:
        abort(400)
    item = {
        'id': items['items'][-1]['id'] + 1,
        'description': request.json['description'],
        'brand': request.json['brand'],
        'model': request.json['model'],
        'quantity': request.json['quantity'],
    }
    items['items'].append(item)
    write_to_json(items)
    response = jsonify({'CREATED':'true'})
    response.status_code = 201
    response.headers['location'] = '/items/%s' %id
    return response

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    items = read_from_json()
    item = [item for item in items['items'] if item['id'] == item_id]

    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['brand'] = request.json.get('brand', item[0]['brand'])
    item[0]['model'] = request.json.get('model', item[0]['model'])
    item[0]['quantity'] = request.json.get('quantity', item[0]['quantity'])


    for item in items['items']:
        if items['items'][item_id-1]['id'] == item['id']:
            items['items'][item_id-1]['brand'] = item['brand']
            items['items'][item_id-1]['description'] = item['description']
            items['items'][item_id-1]['model'] = item['model']
            items['items'][item_id-1]['quantity'] = item['quantity']
    write_to_json(items)
    return jsonify({'UPDATED':'true'}), 201


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = read_from_json()
    item = [item for item in items['items'] if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    items['items'].remove(item[0])
    write_to_json(items)
    return jsonify({'DELETED':'true'})


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port = 5000 ,debug=True)
