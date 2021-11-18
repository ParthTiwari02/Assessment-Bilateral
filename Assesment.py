import os
import time
import shutil
import pymongo
from pymongo import MongoClient

#Initiatiating mongoDb
client = MongoClient('mongodb://127.0.0.1:27017/')

#Creating database with name Assesment
db = client['Assesment']

#Creating Collection
C1 = db.record

#Defining Path 
processing_path = 'D:\Assesment-Bilateral\Processing'
queue_path = 'D:\Assesment-Bilateral\Queue'
processed_path = 'D:\Assesment-Bilateral\Processed'

for i in range(1,61):
    filename = "File" + str(i)+".txt"
    C1.insert_one({"file_number":i,"Processed or not": 0})
    with open(os.path.join(processing_path,filename),"w+") as f:
        pass
    time.sleep(1)
    if(i%5==0):
        files = os.listdir(processing_path)
        for j,file in enumerate(files):
            #moving file from processing folder to queue
            shutil.move(processing_path + "/" + file,queue_path + "/" + file)
            if ((j+1)%5 ==0):
                
                file_in_queue = os.listdir(queue_path)
                for queuefile in file_in_queue:
                    time.sleep(1)
                    shutil.move(queue_path + "/" + queuefile, processed_path + "/" +queuefile)
                    #Updating mongoDB Collection for processed to 1
                    C1.update({"Processed or not": 0},{"$set":{"Processed or not": 1}})               
    