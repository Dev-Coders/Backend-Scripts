from pymongo import MongoClient
import pymongo
import numpy as np
import pandas as pd

client = MongoClient()
db = client.devcoders
population = db.population

def process(cols):
	a = int(cols[0])
	b = int(cols[1])
	c = int(cols[2])
	d = int(cols[3])
	e = int(cols[4])
	f = int(cols[5])
	return int(a+b+c+d+e+f)

def store(cols):
	entry = {}
	entry['State'] = str(cols[0])
	entry['Constituency'] = str(cols[1])
	entry['Total'] = int(cols[2])
	population.insert_one(entry)
	return True

class PreProcess():

	
	def __init__(self):		
		df = pd.read_csv('dataset.csv')
		imp_data = df[['STATE','AC_NAME','18-19 Male','18-19 Female','18-19 Others','Above 18 Male','Above 18 Female','Above 18 Others']]
		imp_data['Total'] = imp_data[['18-19 Male','18-19 Female','18-19 Others','Above 18 Male','Above 18 Female','Above 18 Others']].apply(process,axis=1)
		final_data = imp_data[['STATE','AC_NAME','Total']]
		del (imp_data,df)
		final_data.apply(store,axis=1)
