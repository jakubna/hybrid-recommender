import os
import json
from flask import Flask
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
import logging
import constant
import examples
from flask import jsonify


"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)

logging.basicConfig(filename="logfilename.log", filemode='w', level=logging.DEBUG)

api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='KnowlEdge Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

script_dir = os.path.dirname(__file__)
file_path = "db.json"
db_path = os.path.join(script_dir, file_path)

# recommender request

class RecommenderRequestSchema(Schema):
    task_id = fields.String(required=True,
                            metadata={"example": "046b6c7f-0b8a-43b9",
                                      "description": "Task ID from Knowledge Repository"})
    kpi = fields.String(required=True,
                        metadata={"example": "performance",
                                  "description": "Name of preferable kpi based on which the list should be ranked."})
    performance_metric = fields.String(required=True,
                                       metadata={"example": "predictive_accuracy",
                                                 "description": "Preferable performance metric that shoould be used to select methods."})
    strategy = fields.String(required=True,
                                       metadata={"example": "decisionTreeClassifier",
                                                 "description": "Preferable method to solve a task."})
    task_indicator = fields.String(required=False,
                                       metadata={"example": "oml",
                                                 "description": "Task indicator."})


class RecommenderTrainingRequestSchema(Schema):
    dataset_id = fields.String(required=True,
                            metadata={"example": "1",
                                      "description": "Dataset ID from Knowledge Repository"})
    data_type = fields.String(required=True,
                        metadata={"example": "tabular",
                                  "description": "Data type: tabular, time_series, image."})
    task_type = fields.String(required=True,
                        metadata={"example": "classification",
                                  "description": "Task type: classification, regression, clustering, optimisation."})
    kpi = fields.String(required=True,
                        metadata={"example": "performance",
                                  "description": "Name of preferable kpi based on which the list should be ranked."})
    performance_metric = fields.String(required=True,
                                       metadata={"example": "predictive_accuracy",
                                                 "description": "Preferable performance metric that shoould be used to select methods."})
    strategy = fields.String(required=True,
                                       metadata={"example": "decisionTreeClassifier",
                                                 "description": "Preferable method to solve a task."})
    task_indicator = fields.String(required=False,
                                       metadata={"example": "oml",
                                                 "description": "Task indicator."})


# recommender response
class KpiSchema(Schema):
    performance = fields.Float(required=False,
                        metadata={"example": 0.9,
                                  "description": "value of the performance metric"})
    avg_performance = fields.Float(required=False,
                        metadata={"example": 0.75,
                                  "description": "average performance of a model "})

    priority = fields.Integer(required=False,
                        metadata={"example": 1,
                                  "description": "computation priority"})
    avg_training_time = fields.Float(required=False,
                        metadata={"example": 144.1,
                                  "description": "average value of the execution time"})
    complexity = fields.String(required=False,
                        metadata={"example": "n",
                                  "description": "computational complexity"})


class RecommendationSchema(Schema):
    task_id = fields.String(required=False,
                            metadata={"example": "046b6c7f-0b8a-43b9",
                                      "description": "Task ID"})
    strategy_id = fields.String(required=False,
                            metadata={"example": "096b6c7f-9a6c-32c8",
                                      "description": "Strategy ID"})
    method = fields.String(required=True,
                            metadata={"example": "svm",
                                      "description": "Recommended method"})
    method_setup = fields.String(required=False,
                            metadata={"example": "{'C': 1.0,  'kernel': 'rbf', 'degree': 3}",
                                      "description": "Recommended method setup"})
    kpi = fields.Nested(KpiSchema)


# noinspection PyTypeChecker
class RecommenderResponseSchema(Schema):
    recommendations = fields.List(fields.Nested(RecommendationSchema))


# task type schema

class TaskTypeSchema(Schema):
    task_type_all = fields.List(fields.String(), required=True)

# data type schema

class DataTypeSchema(Schema):
    data_type_all = fields.List(fields.String(), required=True)


# kpi schema
class KpiListSchema(Schema):
    kpi_all = fields.List(fields.String(), required=True)

# performance metric schema

class PerformanceMetricSchema(Schema):
    classification = fields.List(fields.String(), required=False)
    regression = fields.List(fields.String(), required=False)
    clustering = fields.List(fields.String(), required=False)
    optimisation = fields.List(fields.String(), required=False)

# strategy schema

class StrategySchema(Schema):
    tabular_classification = fields.List(fields.String(), required=False)
    tabular_regression = fields.List(fields.String(), required=False)
    tabular_clustering = fields.List(fields.String(), required=False)
    tabular_optimisation = fields.List(fields.String(), required=False)
    time_series_classification = fields.List(fields.String(), required=False)
    time_series_regression = fields.List(fields.String(), required=False)
    time_series_clustering = fields.List(fields.String(), required=False)
    image_classification = fields.List(fields.String(), required=False)

# recommender API definitions
class RecommenderAPI(MethodResource, Resource):
    @doc(description='Recommender POST API for deploying.', tags=['recommendations'])
    @use_kwargs(RecommenderRequestSchema, location=('json'))
    @marshal_with(RecommendationSchema)  # marshalling
    def post(self, **kwargs):
        """
        Get method represents a GET API method
        """
        return jsonify(examples.recommendations_example)


class RecommenderTrainingAPI(MethodResource, Resource):
    @doc(description='Recommender POST API for training.', tags=['recommendations'])
    @use_kwargs(RecommenderTrainingRequestSchema, location=('json'))
    @marshal_with(RecommendationSchema)  # marshalling
    def post(self, **kwargs):
        """
        Get method represents a GET API method
        """

        return jsonify(examples.recommendations_example)


# recommender lists API definitions

class TaskTypeAPI(MethodResource, Resource):
    @doc(description='List all task types.', tags=['lists'])
    @marshal_with(TaskTypeSchema)
    def get(self):
        """
        Get method represents a GET API method
        """
        with open(db_path) as f:
            db = json.load(f)
        return jsonify(db["task_type"])


class DataTypeAPI(MethodResource, Resource):
    @doc(description='List all data types.', tags=['lists'])
    @marshal_with(DataTypeSchema)
    def get(self):
        """
        Get method represents a GET API method
        """
        with open(db_path) as f:
            db = json.load(f)
        return jsonify(db["data_type"])


class KpiListAPI(MethodResource, Resource):
    @doc(description='List all KPIs.', tags=['lists'])
    @marshal_with(KpiListSchema)
    def get(self):
        """
        Get method represents a GET API method
        """
        with open(db_path) as f:
            db = json.load(f)
        return jsonify(db["kpi"])


class PerformanceMetricAPI(MethodResource, Resource):
    @doc(description='List all performance metrics.', tags=['lists'])
    @marshal_with(PerformanceMetricSchema)
    def get(self):
        """
        Get method represents a GET API method
        """
        with open(db_path) as f:
            db = json.load(f)
        return jsonify(db["performance_metric"])


class StrategyAPI(MethodResource, Resource):
    @doc(description='List all strategies.', tags=['lists'])
    @marshal_with(StrategySchema)
    def get(self):
        """
        Get method represents a GET API method
        """
        with open(db_path) as f:
            db = json.load(f)
        return jsonify(db["strategy"])


@app.route('/')
def hello():
    return {'hello': 'world'}


api.add_resource(RecommenderAPI, '/recommender')
api.add_resource(RecommenderTrainingAPI, '/recommender-training')
api.add_resource(TaskTypeAPI, '/list/task_type')
api.add_resource(DataTypeAPI, '/list/data_type')
api.add_resource(KpiListAPI, '/list/kpi')
api.add_resource(PerformanceMetricAPI, '/list/performance_metric')
api.add_resource(StrategyAPI, '/list/strategy')


docs.register(RecommenderAPI)
docs.register(RecommenderTrainingAPI)
docs.register(TaskTypeAPI)
docs.register(DataTypeAPI)
docs.register(KpiListAPI)
docs.register(PerformanceMetricAPI)
docs.register(StrategyAPI)


if __name__ == '__main__':
    app.run(port=8020)
