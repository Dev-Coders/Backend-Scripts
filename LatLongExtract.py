import pandas as pd
import numpy as np
import os
from geopy import geocoders
from geopy.geocoders import Nominatim

data = pd.read_csv("./delhi.csv", sep='$')
#data["Address"]=str(" ")

geolocator = Nominatim()

not_processed = []

for i in range(70):
    
    x = data.get_value(i, "Name").lower()
    x+=", delhi"
    
    try:
        location = geolocator.geocode(x)
        
        data.set_value(i,"Address",str(location.address))
        data.set_value(i,"Latitude",location.latitude)
        data.set_value(i,"Longitude",location.longitude)
    except:
        not_processed.append(i)

data.to_csv("./mydelhi.csv", sep='$')
