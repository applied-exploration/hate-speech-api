from flask import Flask
from flask_restful import Api

from endpoints.inference import ModelEndpoint

app = Flask(__name__)
api = Api(app)


api.add_resource(ModelEndpoint, '/detect') 
