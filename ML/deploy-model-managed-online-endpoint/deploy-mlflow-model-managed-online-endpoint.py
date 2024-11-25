from azure.ai.ml.entities import Model, ManagedOnlineDeployment
from azure.ai.ml.constants import AssetTypes

# create a blue deployment
model = Model(
    path="./model",
    type=AssetTypes.MLFLOW_MODEL,
    description="my mlflow model",
)

blue_deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="endpoint-example",
    model=model,
    instance_type="Standard_F4s_v2",   #VM size
    instance_count=1,  #Number of instances to use
)

ml_client.online_deployments.begin_create_or_update(blue_deployment).result()


#route 100% traffic to a specific deployment
endpoint.traffic = {"blue": 100}. # blue deployment takes 100 traffic
ml_client.begin_create_or_update(endpoint).result()


#delete the endpoint and all associated deployments,
ml_client.online_endpoints.begin_delete(name="endpoint-example")