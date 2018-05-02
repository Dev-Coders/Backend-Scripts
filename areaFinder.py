import pandas as pd
import googlemaps
import private
import pickle
from geopy.distance import vincenty


class Tree:
    def __init__(self, node):
        self.left = None
        self.right = None
        self.data = node


def insert(root, val, flag):
    if root == None:
        return Tree(val)
     
    if val[flag+6] <= root.data[flag+6]:
        root.left = insert(root.left, val, flag^1)
    else:
        root.right = insert(root.right, val, flag^1)
    
    return root

def createSearchTree():
        
    root = None
    data=pd.read_csv("delhi.csv",'$')
    
    node=()
    for row in data.itertuples():
        node = tuple(row)
        root = insert(root, node, 0)
       
    return root


def searchTree(root, location, flag):
    
    if location[flag] < root.data[flag+6]:
        
        if root.left==None:
            return root 
        
        root_dis = vincenty(location, root.data[6:8]).miles
        l_dis = vincenty(location, root.left.data[6:8]).miles
        
        #root_dis = gmaps.directions(location, root.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']
        #l_dis = gmaps.directions(location, root.left.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']
        
        if l_dis < root_dis:
            return searchTree(root.left, location, flag^1)
        else:
            left = root.left
            right = root.right
            
            while left.right:
                    left=left.right
            if right:
                while right.left:
                    right=right.left
                
                #if gmaps.directions(location, left.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value'] < gmaps.directions(location, right.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']:
                if vincenty(location, left.data[6:8]).miles < vincenty(location, right.data[6:8]).miles:
                    if vincenty(location, left.data[6:8]).miles < vincenty(location, root.data[6:8]).miles:
                        return left
                    else:
                        return root
                else:
                    if vincenty(location, right.data[6:8]).miles < vincenty(location, root.data[6:8]).miles:
                        return right
                    else:
                        return root
            
            else:
                return left
    
    elif location[flag] > root.data[flag+6]:
        
        if root.right==None:
            return root 
        
        root_dis = vincenty(location, root.data[6:8]).miles
        r_dis = vincenty(location, root.right.data[6:8]).miles
        
        #root_dis = gmaps.directions(location, root.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']
        #r_dis = gmaps.directions(location, root.right.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']
        
        if r_dis < root_dis:
            return searchTree(root.right, location, flag^1)
        else:
            left = root.left
            right = root.right
            
            while right.left:
                    right=right.left
            if left:
                while left.right:
                    left=left.right
                
                #if gmaps.directions(location, left.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value'] < gmaps.directions(location, right.data[6:8], mode="driving", avoid="ferries")[0]['legs'][0]['distance']['value']:
                if vincenty(location, left.data[6:8]).miles < vincenty(location, right.data[6:8]).miles:
                    if vincenty(location, left.data[6:8]).miles < vincenty(location, root.data[6:8]).miles:
                        return left
                    else:
                        return root
                else:
                    if vincenty(location, right.data[6:8]).miles < vincenty(location, root.data[6:8]).miles:
                        return right
                    else:
                        return root
            
            else:
                return right
        
    else:
        return root

def gmapDistance(loc1,loc2):
    
    gmaps = googlemaps.Client(key=private.MapKey)
    directions_result = gmaps.directions(loc1, loc2, mode="driving", avoid="ferries")

    return (directions_result[0]['legs'][0]['distance']['text'],directions_result[0]['legs'][0]['duration']['text'])


def ReturnConstituency(latitude, longitude):

    with open('tree.pickle', 'rb') as handle:
        root = pickle.load(handle)

    node = searchTree(root, [latitude, longitude], 0)

    ans={}

    ans["Distance"],ans["Time"] = gmapDistance([node.data[6], node.data[7]],[latitude, longitude])

    ans["Latitude"]=node.data[6]
    ans["Longitude"]=node.data[7]
    ans["Address"]=node.data[8]
    ans["Name"]=node.data[4]

    return ans