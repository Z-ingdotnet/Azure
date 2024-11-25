#Trigger the batch scoring job
from azure.ai.ml import Input
from azure.ai.ml.constants import AssetTypes

input = Input(type=AssetTypes.URI_FOLDER, path="azureml:new-data:1")

job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name, 
    input=input)



'''
troubleshoot the scoring script
logs/user/ folder 

job_error.txt: Summarize the errors in your script.
job_progress_overview.txt: Provides high-level information about the number of mini-batches processed so far.
job_result.txt: Shows errors in calling the init() and run() function in the scoring script.
'''