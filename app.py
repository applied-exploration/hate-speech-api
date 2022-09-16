from flask import Flask
from flask_restful import Api

from endpoints.inference import ModelEndpoint
from endpoints.inference import PipelineInfoEndpoint

app = Flask(__name__)
api = Api(app)


api.add_resource(ModelEndpoint, '/detect')  
api.add_resource(PipelineInfoEndpoint, '/pipeline')  

   