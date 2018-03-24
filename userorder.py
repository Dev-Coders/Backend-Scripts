from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pymongo import MongoClient
import pymongo
from bson import json_util
import areaFinder

'''
Need to add authentication lateer!!
'''


class Order(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('UserName', type=str, required=True,
			help='No Username Provided', location='json')
		self.reqparse.add_argument('Latitude', type=float, required=True,
			help='Invalid Location', location='json')
		self.reqparse.add_argument('Longitude', type=float, required=True,
			help='Invalid Location', location='json')
		super(Order, self).__init__()


	def post(self):
		client = MongoClient()
		db = client.devcoders
		orders = db.orders

		username = request.json['UserName']
		latitude = request.json['Latitude']
		longitude = request.json['Longitude']

		nearestConstituency = areaFinder.ReturnConstituency(latitude,longitude)


		order = {
		'UserName':username,
		'Latitude':latitude,
		'Longitude':longitude,
		'NearestConstituencyLatitude':nearestConstituency['Latitude'],
		'NearestConstituencyLongitude':nearestConstituency['Longitude'],
		'NearstConstituencyAddress':nearestConstituency['Address']
		}

		orders.insert_one(order)

		return {'inserted':'order'},201

	def get(self):
		client = MongoClient()
		db = client.devcoders
		orders = db.orders

		result = orders.find()

		final = []
		for i in result:
			i.pop('_id')
			final.append(i)

		return {'Orders':final},200

	def delete(self):
		client = MongoClient()
		db = client.devcoders
		orders = db.orders
		orders.remove()
		return {'deleted':'all'},200


