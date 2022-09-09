from flask import Flask
from flask_restful import Api

from endpoints.inference import ModelEndpoint

app = Flask(__name__)
api = Api(app)


api.add_resource(ModelEndpoint, '/detect') 


# if __name__ == '__main__':
#     app.run()  # run our Flask app
    

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello Sammy!'