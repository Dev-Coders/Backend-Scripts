from pymongo import MongoClient
import pymongo
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import json

client = MongoClient()
db = client.devcoders
population = db.population



def store(cols):
	entry = {}
	entry['State'] = str(cols[0])
	entry['Constituency'] = str(cols[1])
	entry['Total'] = int(cols[2])
	entry['Latitude'] = float(cols[3])
	locators = Nominatim()
	location = locators.geocode(entry['Constituency'])
	entry['Latitude'] = location.latitude
	entry['Longitude'] = location.longitude
	population.insert_one(entry)
	return True


class PreProcess():

	
	def __init__(self):		
		df = pd.read_csv('delhi.csv','$')
		df = df.drop(['Unnamed: 0','Unnamed: 0.1'], axis=1)
		#imp_data = df[['STATE','AC_NAME','18-19 Male','18-19 Female','18-19 Others','Above 18 Male','Above 18 Female','Above 18 Others']]
		#imp_data['Total'] = imp_data[['18-19 Male','18-19 Female','18-19 Others','Above 18 Male','Above 18 Female','Above 18 Others']].apply(process,axis=1)
		#final_data = imp_data[['STATE','AC_NAME','Total']]
		#del (imp_data,df)
		#df.apply(store,axis=1)
		population.remove()
		population.insert(json.loads(df.to_json(orient='records')))




