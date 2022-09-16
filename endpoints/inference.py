from re import A
from flask_restful import Resource, reqparse
import pandas as pd
import ast
from typing import Tuple, List, Optional
import random
from mopi.blocks.pipeline import Pipeline
from mopi.blocks.io import load_pipeline
from mopi.inference import run_inference
from mopi.library.experiments.hate_speech_baselines import random, all_0s, all_1s
from mopi.constants import Const
from mopi.type import SourceTypes

from os import listdir
from os.path import isfile, join
from mopi.utils.hierarchy import hierarchy_to_str

def get_args(keys:List[str])->list:
    parser = reqparse.RequestParser()  # initialize

    for key in keys:
        parser.add_argument(key, required=True, location='args')  # add args
    
    args = parser.parse_args()  # parse arguments to dictionary

    return [args[key] for key in keys]


class PipelineStore:
    def __init__(self):
        self.pipelines: dict[str, Pipeline]= {"random":random, "all_0s": all_0s, "all_1s":all_1s}
        
pipeline_store = PipelineStore()

def get_pipeline(pipeline_name: str, pipeline_store: PipelineStore)->Optional[Pipeline]:
    available_models =  [f.replace(".pth","") for f in listdir(Const.output_pipelines_path) if isfile(join(Const.output_pipelines_path, f))] + list(pipeline_store.pipelines.keys())
    
    if pipeline_name not in available_models:
       return None

    elif pipeline_name in pipeline_store.pipelines.keys():
        print("getting it from dict") 
        pipeline = pipeline_store.pipelines[pipeline_name]
    else: 
        print("Loading it")
        pipeline = load_pipeline(pipeline_name)
        pipeline_store.pipelines[pipeline_name] = pipeline
        
    return pipeline
        
class ModelEndpoint(Resource):
    def __init__(self) -> None:
        self.pipelines:PipelineStore = pipeline_store
    
    def load(self)->None:
        pass
        
    def get(self)->Tuple[dict, int]:
        text, pipeline_name = get_args(['text', 'pipeline_name'])
        queried_texts = text.split(";")

        pipeline = get_pipeline(pipeline_name, self.pipelines)
        if pipeline is None:
            return {
                'message': f"{pipeline_name} is not available."
            }, 409 
        else:
            results = run_inference(pipeline, queried_texts) 
            predictions = {queried_texts[i]: str(result) for i, result in enumerate(results)}

            return {'result': predictions}, 200  # return data with 200 OK 

class PipelineInfoEndpoint(Resource):
    def __init__(self) -> None:
        self.pipelines:PipelineStore = pipeline_store
    
    def get(self)->Tuple[dict, int]:
        pipeline_name = get_args(['pipeline_name'])[0]
        
        pipeline = get_pipeline(pipeline_name, self.pipelines)
        if pipeline is None:
            return {
                'message': f"{pipeline_name} is not available."
            }, 409 
        else:
            full_pipeline = pipeline.children(SourceTypes.fit)
            
            return {'hierarchy': hierarchy_to_str(full_pipeline)}, 200