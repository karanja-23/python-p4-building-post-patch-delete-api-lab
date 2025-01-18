#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakery():

    if request.method == 'GET':
        my_bakeries = []
        for bakery in BakedGood.query.all():
            
            my_bakeries.append(bakery.to_dict())
            
        response = make_response(
            my_bakeries,
            200,
            {'Content-Type':'application/json'}
        )
        return response
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakeries(id):

    if request.method == 'GET':
        my_bakeries = []
        for bakery in Bakery.query.all():
            
            my_bakeries.append(bakery.to_dict())
            
        response = make_response(
            my_bakeries,
            200,
            {'Content-Type':'application/json'}
        )
        return response
    if request.method == 'PATCH':
        for attr in request.form:
            setattr(Bakery.query.filter_by(id=id).first(), attr, request.form.get(attr))
        db.session.commit()
        response = make_response(
            Bakery.query.filter_by(id=id).first().to_dict(),
            200,
            {'Content-Type':'application/json'}
        )
        return response
   
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

    if request.method == 'GET':
        my_bakeries = []
        for bakery in BakedGood.query.all():
            
            my_bakeries.append(bakery.to_dict())
            
        response = make_response(
            my_bakeries,
            200,
            {'Content-Type':'application/json'}
        )
        return response
    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get('name'),
            price=request.form.get('price'),
            created_at=request.form.get('created_at'),
            updated_at=request.form.get('updated_at'),
            bakery_id=request.form.get('bakery_id')
        )
        db.session.add(new_baked_good)
        db.session.commit()
        response = make_response(
            new_baked_good.to_dict(),
            201,
            {'Content-Type':'application/json'}
        )
        return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/<int:id>',methods=['GET','DELETE'])
def baked_good_by_id(id):
    if request.method == 'DELETE':
        baked_good = BakedGood.query.filter(BakedGood.id==id).first()
        db.session.delete(baked_good)
        db.session.commit()
        
        response_body = {
            "delete-succesfull":True,
            "message": "review deleted"
        }
        response = make_response(
            response_body,
            200,
            {'Content-Type':'application/json'}
        )
        return response
        
    
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)