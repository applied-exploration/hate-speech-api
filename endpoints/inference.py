from flask_restful import Resource, reqparse
import pandas as pd
import ast
from typing import Tuple
import random

class RandomModel:
    def infer(self, text: str)->Tuple[int, list[float]]:
        random_category = random.randint(0, 1)
        return random_category,[0.1,0.0] if random_category == 0 else [0.0,1.0]

class ModelEndpoint(Resource):
    def __init__(self)->None:
        self.model = RandomModel()
    
    def load(self)->None:
        pass
        
    def get(self)->Tuple[dict, int]:
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('text', required=True, location='args')  # add args
        
        args = parser.parse_args()  # parse arguments to dictionary
   
        queried_text = args['text']
        
        result = self.model.infer(queried_text)



        return {'result': result}, 200  # return data with 200 OK 
               