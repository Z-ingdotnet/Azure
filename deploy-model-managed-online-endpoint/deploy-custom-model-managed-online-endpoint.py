'''
model files
scoring script
environment
create the deployment
'''


#Create the scoring script

import json
import joblib
import numpy as np
import os

# called when the deployment is created or updated / e.g. when the service is initialized.
def init():  
    global model
    # get the path to the registered model file and load it
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    model = joblib.load(model_path)

# called when a request is received/when new data is submitted to the service.
def run(raw_data): 
    # get the input data as a numpy array
    data = np.array(json.loads(raw_data)['data'])
    # get a prediction from the model
    predictions = model.predict(data)
    # return the predictions as any JSON serializable format
    return predictions.tolist()


#Create an environment

''' define the Conda dependencies 

conda.yml file:
name: basic-env-cpu
channels:
  - conda-forge
dependencies:
  - python=3.7
  - scikit-learn
  - pandas
  - numpy
  - matplotlib
'''

#create the environment,
from azure.ai.ml.entities import Environment

env = Environment(
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_file="./src/conda.yml",
    name="deployment-environment",
    description="Environment created from a Docker image plus Conda environment.",
)
ml_client.environments.create_or_update(env)


#Create the deployment
from azure.ai.ml.entities import ManagedOnlineDeployment, CodeConfiguration

model = Model(path="./model",

blue_deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="endpoint-iz",
    model=model,
    environment="deployment-environment",
    code_configuration=CodeConfiguration(
        code="./src", scoring_script="score.py"
    ),
    instance_type="Standard_DS2_v2",
    instance_count=1,
)

ml_client.online_deployments.begin_create_or_update(blue_deployment).result()



#deploy multiple models to an endpoint
endpoint.traffic = {"blue": 100}  # blue deployment takes 100 traffic
ml_client.begin_create_or_update(endpoint).result()


ml_client.online_endpoints.begin_delete(name="endpoint-iz")