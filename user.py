from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Api, Resource, marshal, reqparse, fields
from pymongo import MongoClient
import pymongo
from bson import json_util

'''
Need to change GET and add auth in it. New class
'''

class User(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('UserName', type=str, required=True,
			help='No username provided', location='json')
		self.reqparse.add_argument('PassWord', type=str, required=True,
			help='No PassWord provided', location='json')

	def post(self):
		client = MongoClient()
		db = client.devcoders
		users = db.users

		username = request.json['UserName']
		password = request.json['PassWord']

		user = {}
		user['UserName'] = username
		user['PassWord'] = password

		users.insert_one(user)

		return {'Registered':'User'},201

	def get(self):
		client = MongoClient()
		db = client.devcoders
		users = db.users

		result = users.find()

		return {'Users':json_util._json_convert([i for i in result])},200