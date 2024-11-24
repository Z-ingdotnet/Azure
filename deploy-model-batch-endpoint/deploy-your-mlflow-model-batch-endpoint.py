#Register an MLflow model
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

model_name = 'mlflow-model'
model = ml_client.models.create_or_update(
    Model(name=model_name, path='./model', type=AssetTypes.MLFLOW_MODEL)
)



#Deploy an MLflow model to an endpoint


from azure.ai.ml.entities import BatchDeployment, BatchRetrySettings
from azure.ai.ml.constants import BatchDeploymentOutputAction

deployment = BatchDeployment(
    name="forecast-mlflow",
    description="A sales forecaster",
    endpoint_name=endpoint.name,
    model=model,
    compute="aml-cluster",
    instance_count=2,  #Count of compute nodes to use for generating predictions.
    max_concurrency_per_instance=2, #Maximum number of parallel scoring script runs per compute node.
    mini_batch_size=2, #Number of files passed per scoring script run.
    output_action=BatchDeploymentOutputAction.APPEND_ROW,  #What to do with the predictions: summary_only or append_row
    output_file_name="predictions.csv", #File to which predictions will be appended, if you choose append_row for output_action.
    retry_settings=BatchRetrySettings(max_retries=3, timeout=300),
    logging_level="info",
)
ml_client.batch_deployments.begin_create_or_update(deployment)