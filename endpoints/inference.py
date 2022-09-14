from flask_restful import Resource, reqparse
import pandas as pd
import ast
from typing import Tuple
import random
from mopi.blocks.pipeline import Pipeline
from mopi.blocks.io import load_pipeline
from mopi.inference import run_inference
from mopi.library.experiments.hate_speech import random, all_0s, all_1s
from mopi.constants import Const

from os import listdir
from os.path import isfile, join


class ModelEndpoint(Resource):
    def __init__(self) -> None:
        self.pipelines:dict[str, Pipeline] = {"random":random, "all_0s": all_0s, "all_1s":all_1s}
    
    def load(self)->None:
        pass
        
    def get(self)->Tuple[dict, int]:
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('text', required=True, location='args')  # add args
        parser.add_argument('pipeline_name', required=True, location='args')  # add args
        
        args = parser.parse_args()  # parse arguments to dictionary
   
        queried_texts = args['text'].split(";")
        pipeline_name = args['pipeline_name']
        
        available_models =  [f.replace(".pth","") for f in listdir(Const.output_pipelines_path) if isfile(join(Const.output_pipelines_path, f))] + list(self.pipelines.keys())
        
        if pipeline_name not in available_models:
            return {
                'message': f"{pipeline_name} is not available."
            }, 409 
        
        if pipeline_name in self.pipelines.keys():
            print("getting it from dict") 
            pipeline = self.pipelines[pipeline_name]
        else: 
            print("Loading it")
            pipeline = load_pipeline(pipeline_name)
            self.pipelines[pipeline_name] = pipeline
        
          
        results = run_inference(pipeline, queried_texts)
   
        predictions = {queried_texts[i]: str(result) for i, result in enumerate(results)}

        return {'result': predictions}, 200  # return data with 200 OK 
               