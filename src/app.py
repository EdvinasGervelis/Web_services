#!flask/bin/python
from flask import Flask, abort
from flask import jsonify
from flask import make_response
from flask import request
import json
import requests
import copy
import urllib.request


app = Flask(__name__)


items = [
    {
        "brand": "Samsung",
        "description": "microwave",
        "id": 1,
        "model": "super hot 2000",
        "quantity": 12,
        "orders": [
            "1",
            "2"
        ]
    },
    {
        "brand": "Philips",
        "description": "TV",
        "id": 2,
        "model": "e540",
        "quantity": 1,
        "orders": [
            "1"
        ]
    },
    {
        "brand": "Suzuki",
        "description": "microwave",
        "id": 3,
        "model": "super hot 2000",
        "quantity": 12,
        "orders": [
            "1"
        ],

    },
    {
        "brand": "Samsung",
        "description": "microwave",
        "id": 4,
        "model": "super hot 2000",
        "quantity": 12,
        "orders": [
            "1"
        ]
    }
]

# embedded

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/items', methods=['GET'])
def get_items():
    #items = read_from_json()
    itemss = copy.deepcopy(items)
    customersMas = []
    if( request.args.get('embedded','') == 'orders'):
        for item in itemss:
            customersMas = []
            for customer in item['orders']:
                url = 'http://web2:80/visits/schedules/%s' %customer
                r = requests.get(url)
                customers = r.text
                print(customers)
                data = json.loads(customers)
                customersMas.append(data)
            item['orders'] = customersMas

    return jsonify(itemss)

@app.route('/items', methods = ['GET'])
def search_embedded():
    print ("labas")




@app.route('/items/<int:item_id>/orders', methods=['GET'])
def get_items_orders(item_id):
    customers = []
    custo = []
    msg= ""
    url = 'http://web2:80/visits/schedules'
    r = requests.get(url)
    customers = r.text
    data = json.loads(customers)
    for item in items:
        if item['id'] == item_id:
            for order in item['orders']:
                try:
                    url_test = 'http://web2:80/visits/schedules/%s' %order
                    r_test = requests.get(url_test)
                    customers_test = r_test.text
                    data_test = json.loads(customers_test)
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    return not_found(404)
                # print(order)
                for customer in data:
                    if order == customer['ID']:
                        custo.append(customer)
    msg = jsonify(custo)
    return msg

@app.route('/items/<int:item_id>/orders/<int:customer_id>', methods=['GET'])
def get_item_orders_by_id(item_id, customer_id):
    customers = []
    custo = []
    msg= ""
    try:
        url = 'http://web2:80/visits/schedules/%s' %customer_id
        r = requests.get(url)
        customers = r.text
        data = json.loads(customers)
    except ValueError:
        return not_found(404)

    for item in items:
        if item['id'] == item_id:
            check_item = item
            for order in item['orders']:
                # print(order)
                # print(customer_id)
                if int(order) == customer_id:
                    # print ("labas")
                    data = json.loads(customers)
                    # print (data.__class__.__name__)
    if not data:
        return not_found(404)
    return jsonify(data)



@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = []
    msg = ""
    for it in items:
        if it['id'] == item_id:
            # item = it
            item = copy.deepcopy(it)
            if( request.args.get('embedded','') == 'orders'):
                customersMas = []
                for customer in item['orders']:
                    url = 'http://web2:80/visits/schedules/%s' %customer
                    r = requests.get(url)
                    customers = r.text
                    data = json.loads(customers)
                    customersMas.append(data)
                item['orders'] = customersMas
    if len(item) == 0:
        msg = not_found(404)
    else:
        msg = jsonify(item)

    return msg




@app.route('/items', methods=['POST'])
def create_item():
    #items = read_from_json()
    if not request.json or not 'description'in request.json or not 'brand'in request.json or not 'model'in request.json or not 'quantity' in request.json:
        abort(400)

    for order in request.json.get('orders', []):
        try:
            url = 'http://web2:80/visits/schedules/%s' %order
            r = requests.get(url)
            customers = r.text
            data = json.loads(customers)
        except ValueError:
            return not_found(404)
    item = {
        'id': items[-1]['id'] + 1,
        'description': request.json['description'],
        'brand': request.json['brand'],
        'model': request.json['model'],
        'quantity': request.json['quantity'],
        'orders': request.json.get('orders', []),
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
    if not request.json or not 'description' in request.json  or not 'brand'in request.json or not 'model'in request.json or not 'quantity' in request.json or not 'orders' in request.json:
        abort(400)
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)


    # print(request.json.get('orders', []))
    for order in request.json.get('orders', []):
        try:
            url = 'http://web2:80/visits/schedules/%s' %order
            r = requests.get(url)
            customers = r.text
            data = json.loads(customers)
        except ValueError:
            return not_found(404)

    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['brand'] = request.json.get('brand', item[0]['brand'])
    item[0]['model'] = request.json.get('model', item[0]['model'])
    item[0]['quantity'] = request.json.get('quantity', item[0]['quantity'])
    item[0]['orders'] = request.json.get('orders', item[0]['orders'])

    for item in items:
        if items[item_id-1]['id'] == item['id']:
            items[item_id-1]['brand'] = item['brand']
            items[item_id-1]['description'] = item['description']
            items[item_id-1]['model'] = item['model']
            items[item_id-1]['quantity'] = item['quantity']
            items[item_id-1]['orders'] = item['orders']
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

    if 'orders' in request.json:
        for order in request.json.get('orders', []):
            try:
                url = 'http://web2:80/visits/schedules/%s' %order
                r = requests.get(url)
                customers = r.text
                data = json.loads(customers)
            except ValueError:
                return not_found(404)
    item[0]['orders'] = request.json.get('orders', item[0]['orders'])

    # print(items)

    for item in items:
        # print(item)
        if items[item_id-1]['id'] == item['id']:
            items[item_id-1]['brand'] = item['brand']
            items[item_id-1]['description'] = item['description']
            items[item_id-1]['model'] = item['model']
            items[item_id-1]['quantity'] = item['quantity']
            items[item_id-1]['orders'] = item['orders']
    #write_to_json(items)
    return jsonify({'UPDATED':'true'}), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    #items = read_from_json()
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    items.remove(item[0])
    # print(items)
    #write_to_json(items)
    return jsonify({'DELETED':'true'})

@app.route('/items/<int:item_id>/orders/<int:customer_id>', methods=['DELETE'])
def delete_item_by_order(item_id, customer_id):
    check_item = []
    order_id = ""
    for item in items:
        if item['id'] == item_id:
            check_item = item
            for order in item['orders']:
                if int(order) == customer_id:
                    order_id = customer_id
                    item['orders'].remove(order)
    if len(check_item) == 0 or order_id == "":
        abort(404)

    return jsonify({'DELETED':'true'})


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port = 5000 ,debug=True)
