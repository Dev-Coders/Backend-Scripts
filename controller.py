from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pojo import PreProcessData
from userorder import Order
from user import User
import areaFinder
import pickle
# import areaFinder
# import pickle



app = Flask(__name__)
api = Api(app)



root=areaFinder.createSearchTree()

with open('tree.pickle', 'wb') as handle:
    pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)
# root=areaFinder.createSearchTree()

# with open('tree.pickle', 'wb') as handle:
#     pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)

#-----------FLASK----ROUTES----------


api.add_resource(PreProcessData, '/preprocess', endpoint='preprocess')
api.add_resource(Order, '/order', endpoint='order')
api.add_resource(User, '/user', endpoint='user')


if __name__ == '__main__':
	app.run(port=5000,use_reloader=True)
