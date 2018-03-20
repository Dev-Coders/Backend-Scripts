from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pojo import PreProcessData

app = Flask(__name__)
api = Api(app)




#-----------FLASK----ROUTES----------

api.add_resource(PreProcessData, '/preprocess', endpoint='preprocess')


if __name__ == '__main__':
	app.run(port=5000,use_reloader=True)