'''
COMMON FUNCTIONALITY
'''

import base64
from urllib.parse import quote
import pymongo
from flask import Flask
from flask_restful import Api

PWD = base64.b64decode("QW56aGVsYUBLQG1wcjJPMjMh".encode('ascii')).decode('ascii') # write your password, please, you can do it explicitly without encode-mechanism I wrote.
CLIENT = pymongo.MongoClient(f"mongodb://root:{quote(PWD)}@127.0.0.1:27017/")
REG_APP = Flask(__name__)
API = Api(REG_APP)
DB = CLIENT["Cloud"] # Your DB name should be "Cloud", or change the hard-coded one, please.

def create_collection(collection_name):
    try:
        DB.create_collection(collection_name)
    except CollectionInvalid:
        print("Unable create the collection.")
