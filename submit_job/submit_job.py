from azure.ai.ml import command

# configure job
job = command(
    code="./src",
    command="train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="train-model",
    experiment_name="train-classification-model"
    )

# submit job
returned_job = ml_client.create_or_update(job)