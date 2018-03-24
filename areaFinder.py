import pandas as pd
from geopy.distance import distance

def ReturnConstituency(latitude, longitude):
    
    data = pd.read_csv("./delhi.csv", sep='$')
    
    b=False
    x=0; addr=""
    loc=()
    
    my_loc = (float(latitude), float(longitude))
    for row in data.iterrows():
        
        temp_loc = (float(row[1]["Latitude"]), float(row[1]["Longitude"]))
        dist = distance(my_loc,temp_loc).miles
        
        if not b:
            loc=temp_loc
            x=dist
            addr=row[1]["Address"]
            b=True
        else:
            if x>dist:
                x=dist
                loc=temp_loc
                addr=row[1]["Address"]
        
    ans={}
    ans["Latitude"], ans["Longitude"]=loc
    ans["Address"]=addr
    
    return ans