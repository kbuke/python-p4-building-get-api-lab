#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_data = bakery.to_dict()
        return jsonify(bakery_data), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    all_baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(desc("price")).all()]
    return make_response(all_baked_goods,200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc("price")).limit(1).first()
    baked_good_dict = baked_good.to_dict()    
    return make_response(baked_good_dict, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
