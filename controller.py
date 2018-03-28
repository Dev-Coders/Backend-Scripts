from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pojo import PreProcessData
from userorder import Order
from user import User
<<<<<<< HEAD
import areaFinder
import pickle
=======
# import areaFinder
# import pickle
>>>>>>> 7f492dc5476ea7d8036d8be297dc9aae33f63a97



app = Flask(__name__)
api = Api(app)



<<<<<<< HEAD
root=areaFinder.createSearchTree()

with open('tree.pickle', 'wb') as handle:
    pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)
=======
# root=areaFinder.createSearchTree()

# with open('tree.pickle', 'wb') as handle:
#     pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)
>>>>>>> 7f492dc5476ea7d8036d8be297dc9aae33f63a97

#-----------FLASK----ROUTES----------


api.add_resource(PreProcessData, '/preprocess', endpoint='preprocess')
api.add_resource(Order, '/order', endpoint='order')
api.add_resource(User, '/user', endpoint='user')


if __name__ == '__main__':
	app.run(port=5000,use_reloader=True)
