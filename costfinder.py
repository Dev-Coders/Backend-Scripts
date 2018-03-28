import googlemaps
from pymongo import MongoClient
import private

cost_per_km = 3
cost_hiring = 50
number_of_workers = 0
max_orders = 1

workshop = {'Latitude':28.533337,'Longitude':77.273447}

'''
Changes in COSTTTTTT

'''

client = MongoClient()
db = client.devcoders
boys = db.delivery_boys
boys.remove()


class CostFinder():

	def __init__(self):
		self.gmaps = googlemaps.Client(key=private.MapKey)
		pass


	def findcost(self,user):
		

		workers = boys.find()

		#print(list(workers))

		global number_of_workers

		if workers.count()==0:
			ans = self.newWorkerCost(user)
			newCost = (ans['Distance'] * 1.0 / 1000)*cost_per_km + cost_hiring
			number_of_workers += 1

			#print('adding new')

			boy = {
			'id':number_of_workers,
			'name':'temp',
			'currLatitude':workshop['Latitude'],
			'currLongitude':workshop['Longitude'],
			'orders':[
				{
				'Latitude':user['Latitude'],
				'Longitude':user['Longitude'],
				'isCarrying':False,
				'delivery_order':1
				}
			],
			'number_of_orders':1
			}

			boys.insert_one(boy)
			return newCost
		else:
			newDist = self.newWorkerCost(user)

			oldDist = self.bestWorkerCost(user,[worker for worker in workers])

			newCost = (newDist['Distance'] * 1.0 / 1000)*cost_per_km + cost_hiring

			oldCost = (oldDist['Distance'] * 1.0 / 1000)*cost_per_km

			print(newCost,oldCost)

			if newCost<oldCost:
				number_of_workers += 1
				boy = {
				'id':number_of_workers,
				'name':'temp',
				'currLatitude':workshop['Latitude'],
				'currLongitude':workshop['Longitude'],
				'orders':[
					{
					'Latitude':user['Latitude'],
					'Longitude':user['Longitude'],
					'isCarrying':False,
					'delivery_order':1
					}
				],
				'number_of_orders':1
				}

				boys.insert_one(boy)
				return newCost
			else:
				#boys.update_one({},{})
				bestDistID = oldDist['DeliveryBoyID']
				oldWorker = boys.find({'id':bestDistID})

				oldWorker = [w for w in oldWorker]
				oldWorker = oldWorker[0]
				#print(oldWorker['orders'])
				oldWorker['orders'].append(
					{'Latitude':user['Latitude'],
					'Longitude':user['Longitude'],
					'isCarrying':False,
					'delivery_order':1})

				boys.update_one({'id':bestDistID},{'$set':{'orders':oldWorker['orders']},'$inc':{'number_of_orders':1}})
				return oldCost

			

	
	####--------------Cost from workshop to req.


	def newWorkerCost(self,user):
		#selfgmaps = googlemaps.Client(key=private.MapKey)
		
		loc1 = {'lat':workshop['Latitude'],'lng':workshop['Longitude']}
		loc2 = {'lat':user['Latitude'],'lng':user['Longitude']}

		directions_result = self.gmaps.directions(loc1, loc2, mode='driving', avoid='ferries', units='metric')
		directions_result = directions_result[0]['legs'][0]

		ans = {
		'Distance':directions_result['distance']['value']
		}

		return ans



	def getDistanceBetweenOrders(self,loc1,loc2):
		#gmaps = googlemaps.Client(key=private.MapKey)
		directions_result = self.gmaps.directions(loc1, loc2, mode='driving', avoid='ferries', units='metric')
		directions_result = directions_result[0]['legs'][0]
		return directions_result['distance']['value']



	#####---------Cost from not carrying req's to new req.

	def bestWorkerCost(self,user,workers):

		
		bestDist = 100000
		bestDistID = 0

		

		for worker in workers:

			minDist = 100000
			minDistID = 0

			for worker_order in worker['orders']:
				#print(worker_order['isCarrying'])
				if worker_order['isCarrying']==False and worker['number_of_orders']<=max_orders:
					
					loc1 = {'lat':user['Latitude'],'lng':user['Longitude']}
					loc2 = {'lat':worker_order['Latitude'],'lng':worker_order['Longitude']}
					dist = self.getDistanceBetweenOrders(loc1,loc2)
					if dist<minDist:
						#print('true')
						minDist = min(minDist,dist)
						minDistID = worker['id']

			if minDist==100000:
				loc1 = {'lat':user['Latitude'],'lng':user['Longitude']}
				loc2 = {'lat':workshop['Latitude'],'lng':workshop['Longitude']}
				minDist = self.getDistanceBetweenOrders(loc1,loc2)

				loc1 = {'lat':worker['currLatitude'],'lng':worker['currLongitude']}
				loc2 = {'lat':workshop['Latitude'],'lng':workshop['Longitude']}
				minDist += self.getDistanceBetweenOrders(loc1,loc2)
				minDistID = worker['id']

			if minDist<bestDist and minDistID!=0:
				bestDist = minDist
				bestDistID = minDistID

		if bestDistID==0:
			return {'Distance':self.newWorkerCost(user),'DeliveryBoyID':0}

		print(bestDistID)

		
		#print(list(boys.find()))

		ans = {'Distance':bestDist,'DeliveryBoyID':bestDistID}
		return ans

				



a = CostFinder()
print(a.findcost({'Latitude':28.976883,'Longitude':77.700331}))
print()
print(a.findcost({'Latitude':28.538765,'Longitude':77.254660}))
print()
print(a.findcost({'Latitude':28.539125,'Longitude':77.216085}))
print()
print(a.findcost({'Latitude':28.502120,'Longitude':77.260826}))
print()
print(a.findcost({'Latitude':28.976883,'Longitude':77.700331}))
print()
