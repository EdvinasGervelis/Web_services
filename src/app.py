#!flask/bin/python
from flask import Flask, abort
from flask import jsonify
from flask import make_response
from flask import request
import json


app = Flask(__name__)


items = [
    {
        "brand": "Samsung",
        "description": "microwave",
        "id": 1,
        "model": "super hot 2000",
        "quantity": 12
    },
    {
        "brand": "Philips",
        "description": "TV",
        "id": 2,
        "model": "e540",
        "quantity": 1
    },
    {
        "brand": "Suzuki",
        "description": "microwave",
        "id": 3,
        "model": "super hot 2000",
        "quantity": 12
    },
    {
        "brand": "Samsung",
        "description": "microwave",
        "id": 4,
        "model": "super hot 2000",
        "quantity": 12
    }
]
# def read_from_json():
#     items = json.load(open('data.json'))
#     return items
#
# def write_to_json(data):
#     with open('data.json', 'w') as outfile:
#         json.dump(data, outfile)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/items', methods=['GET'])
def get_items():
    #items = read_from_json()
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = []
    msg = ""
    for it in items:
        if it['id'] == item_id:
            item = it
    if len(item) == 0:
        msg = not_found(404)
    else:
        msg = jsonify(item)
    return msg


@app.route('/items', methods=['POST'])
def create_item():
    #items = read_from_json()
    if not request.json or not 'description' or not 'brand' or not 'model' or not 'quantity' in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1,
        'description': request.json['description'],
        'brand': request.json['brand'],
        'model': request.json['model'],
        'quantity': request.json['quantity'],
    }
    items.append(item)
    #write_to_json(items)
    response = jsonify({'CREATED':'true'})
    response.status_code = 201
    response.headers['location'] = '/items/%s' %item['id']
    return response

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    #items = read_from_json()
    item = [item for item in items if item['id'] == item_id]
    if not request.json or not 'description' or not 'brand' or not 'model' or not 'quantity' in request.json:
        abort(400)
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['brand'] = request.json.get('brand', item[0]['brand'])
    item[0]['model'] = request.json.get('model', item[0]['model'])
    item[0]['quantity'] = request.json.get('quantity', item[0]['quantity'])

    for item in items:
        if items[item_id-1]['id'] == item['id']:
            items[item_id-1]['brand'] = item['brand']
            items[item_id-1]['description'] = item['description']
            items[item_id-1]['model'] = item['model']
            items[item_id-1]['quantity'] = item['quantity']
    #write_to_json(items)
    return jsonify({'UPDATED':'true'}), 200


@app.route('/items/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    #items = read_from_json()
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['brand'] = request.json.get('brand', item[0]['brand'])
    item[0]['model'] = request.json.get('model', item[0]['model'])
    item[0]['quantity'] = request.json.get('quantity', item[0]['quantity'])

    print(items)

    for item in items:
        print(item)
        if items[item_id-1]['id'] == item['id']:
            items[item_id-1]['brand'] = item['brand']
            items[item_id-1]['description'] = item['description']
            items[item_id-1]['model'] = item['model']
            items[item_id-1]['quantity'] = item['quantity']
    #write_to_json(items)
    return jsonify({'UPDATED':'true'}), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    #items = read_from_json()
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    items.remove(item[0])
    print(items)
    #write_to_json(items)
    return jsonify({'DELETED':'true'})


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port = 5000 ,debug=True)
