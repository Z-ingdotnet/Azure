
'''
Blue/green deployment=A/B Testing=TEST/Control

'''

'''
Create a managed online endpoints

Model assets: model pickle file, or a registered model in the Azure Machine Learning workspace.
Scoring script: to loads the model.
Environment: lists all necessary packages that need to be installed on the compute of the endpoint.
Compute configuration: the needed compute size + scale settings 

'''


from azure.ai.ml.entities import ManagedOnlineEndpoint

# create an online endpoint
endpoint = ManagedOnlineEndpoint(
    name="endpoint-example",  #Name of the endpoint. Must be unique in the Azure region.
    description="Online endpoint",
    auth_mode="key", #1. key for key-based authentication. 2.aml_token for Azure Machine Learning token-based authentication.
)

ml_client.begin_create_or_update(endpoint).result()