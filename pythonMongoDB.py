from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import time
app=Flask(__name__)
CORS(app)
client=MongoClient('localhost',27017)
db=client.iotlab
alldata=[]
dbdata = db.mydatacollection.find({})
for data in dbdata:
	alldata.append(data)
@app.route('/')
def welcome():
	print ('welcome() user')
	return 'Welcome user to server'
@app.route('/data/',methods=['GET','POST'])
def data():
	print('data() function called')
	if request.method == 'GET':
		return jsonify(alldata)
	elif request.method == 'POST':
		data =request.json
		data["_id"]="pkt_"+str(time.time())
		data["time"] = int(time.time()) * 1000
		result=db.mydatacollection.insert_one(data)
		alldata.append(data)
		print(data)
		return jsonify(data)
@app.route('/data/latest',methods=['GET'])
def getLatest():
	print('getLatest() function called')
	if request.method == 'GET':
		return jsonify(alldata[-1])
if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000)   #host is what type of connection and what should accept , 0.0.0.0 means it can accept every connections
print('Exited')
