from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://10.57.0.92:27017')
db = client['maple_pds']
print('connect maple_pds')

db.finalexam.find({'grade_id': 1})
