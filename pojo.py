from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from pymongo import MongoClient
import pymongo
from preprocess import PreProcess
from bson import json_util

client = MongoClient()
db = client.devcoders
popu = db.population

class PreProcessData(Resource):

	def get(self):
		result = popu.find()
		if result.count()==0:
			return jsonify({'No':'Records Found'}),404
		return {'result':json_util._json_convert([i for i in result])},200

	def post(self):
		popu.drop
		abc = PreProcess()
		return {'inserted':'everything'},301