import pickle
import os

def takeFirst(elem):
    return elem[0]

def calculate_centroid(cluster):
        
    size=len(cluster)
    
    if size == 1:
        return [cluster[0][0], cluster[0][1], size]
    
    cluster.sort(key=takeFirst)
    
    A=0
    x=0;y=0
    for i in range(size):
        temp = (cluster[i][0]*cluster[(i+1)%size][1] - cluster[(i+1)%size][0]*cluster[i][1])
        A += temp
        x += (cluster[i][0]+cluster[(i+1)%size][0])*temp
        y += (cluster[i][1]+cluster[(i+1)%size][1])*temp
    
    if A == 0:
        return [cluster[0][0], cluster[0][1], size]
    
    x//=int(3*A)
    y//=int(3*A)
    
    return [x,y,size]

def new_warehouse():
    
    clusters=[]
    for root, dirs, files, in os.walk("clusters"):
        for cluster in files:
            with open('clusters/'+ cluster, 'rb') as handle:
                clusters.append(pickle.load(handle))


    centroids=[] 
    for cluster in clusters:
        centroids.append(calculate_centroid(cluster))


    temp=0
    x=0;y=0
    for centroid in centroids:
        x += centroid[0]*centroid[2]
        y += centroid[1]*centroid[2]
        temp += centroid[2]

    return [x//temp, y//temp]

#print(new_warehouse())