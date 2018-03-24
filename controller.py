from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pojo import PreProcessData
from userorder import Order
from user import User

app = Flask(__name__)
api = Api(app)




#-----------FLASK----ROUTES----------

api.add_resource(PreProcessData, '/preprocess', endpoint='preprocess')
api.add_resource(Order, '/order', endpoint='order')
api.add_resource(User, '/user', endpoint='user')


if __name__ == '__main__':
	app.run(port=5000,use_reloader=True)