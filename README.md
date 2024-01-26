# Hybrid Strategy Recommender API

## General Description
The Hybrid Strategy Recommender component is dedicated to providing support to the expert in selecting the appropriate strategy 
(machine learning method) for a specific problem (task), considering its nature. These recommendations are prepared in a hybrid way, combining the advantages of two components: an Ontological component and a Reasoning component. 
The Ontological component is where the knowledge about AI methods and Manufacturing problems will be represented in a 
Graph-based formalism. In addition, it has a reasoning component which will exploit the knowledge from the Ontological 
component to make inferences to suggest the best AI methods/strategies and concrete AI models tuned with optimal hyperparameters.

## Metadata

|       |                                           |
| --------- | --------
| version        | v1.0
| contact person | natalia.jakubiak@upc.edu
| download link    | https://github.com/jakubna/hybrid-recommender

## Main Features
We can distinguish two main examples of the use of the system:
* Scenario 1: Training phase. In this case a user in a role of data scientist through User Interface can train the models based on specification of a task, provided data’s descriptors, technical KPIs and optionally a partially filled strategy (for example specification of a preferable algorithm type).
* Scenario 2: Deployment phase. In this scenario a user in a role of a production process specialist can provide information about task at the shopfloor and the best previously trained model will be selected and deployed.

The recommendation process is initialised by establishing meta knowledge based on information about previous machine learning experiments and their results. It includes data descriptors (meta-features extracted from stored datasets), task descriptors (task details), applied strategies (machine learning methods historically used to solve a considered task) and performance metrics (evaluation methods computed for employed strategies, for example, precision). When a new task appears, meta-data for the new training set is calculated. Then, the meta-data is matched to the existing meta-knowledge. As a result of the matching, a recommendation is created containing the most appropriate learning algorithm for the task being considered along with the selected parameters.


## Installation instructions
Code: [link]( https://github.com/jakubna/hybrid-recommender "Repo")

cd hybrid-recommender

docker-compose build

docker-compose up

API: http://localhost:8080/swagger-ui

## OpenAPI link or description
An initial Recommender API has been implemented through a Flask web service to ensure the necessary structure, standards, and mechanisms for enabling integration of the strategy recommendation system with the other components.
We can distinguish two main API endpoints to serve for two scenarios of the use of the system:
* */recommdener-training* - training phase. In this case, a user in the role of data scientist through User Interface can train the models based on the specification of a task, provided data descriptors, technical KPIs and optionally a partially filled strategy (for example specification of a preferable algorithm type). The API endpoint accepts the POST requests with the parameters:
    - dataset_id: id of the dataset in the Knowledge Repository
    - data_type: data type: tabular, time_series, image 
    - task_type: task type: classification, regression, clustering, optimisation 
    - kpi: name of preferable KPI based on which the list should be ranked 
    - performance_metric: preferable performance metric that should be used to select methods 
    - strategy: preferable method to solve a task
    - task_indicator: indicator of the component from which the request comes from
* */recommender* - deployment phase. In this scenario, a user in the role of a production process specialist can provide information about a task on the shop floor and the best previously trained model will be selected and deployed. The API endpoint accepts the POST requests with the parameters:
  - task_id: id of a task in the Knowledge Repository
  - kpi: name of preferable KPI based on which the list should be ranked
  - performance_metric: preferable performance metric that should be used to select methods
  - strategy: preferable method to solve a task
  - task_indicator: indicator of the component from which the request comes from

The framework output is a list of ranked recommendations in JSON format. The recommendation object contains information such as the considered task ID, strategy ID, KPI values, recommended method and method configurations/hyperparameters that might be used for the AI Model Generation component to initialise the model training/tuning process:
* task_id: id of a task in the Knowledge Repository
* strategy_id: recommended strategy id 
* method: recommended method 
* method_setup: recommended method setup 
* kpi: 
  - performance: value of the performance metric
  - avg_performance: average performance of a model
  - priority: computation priority
  - avg_training_time: average value of the execution time
  - complexity: computational complexity.
  - 
Additionally, the component contains the following GET endpoints: 
* */list/data_type*
* */list/kpi*
* */list/performance_metric*
* */list/strategy*
* */list/task_type*

These endpoints were developed for integration purposes, especially smoothing the integration with the user interface. They return the lists of all objects of a given kind available in the case-based repository, e.g. list of all strategies from which will be shown to the user.

Swagger documentation of the API and execution examples can be found at the [link](https://upc.pythonanywhere.com/swagger-ui/ "API doc").

