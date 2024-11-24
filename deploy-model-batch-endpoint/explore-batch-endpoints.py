# create a batch endpoint
endpoint = BatchEndpoint(
    name="endpoint-2",
    description="A batch endpoint",
)

ml_client.batch_endpoints.begin_create_or_update(endpoint)



#compute clusters for batch deployments
from azure.ai.ml.entities import AmlCompute

cpu_cluster = AmlCompute(
    name="aml-cluster",
    type="amlcompute",
    size="STANDARD_DS11_V2",
    min_instances=0,
    max_instances=4,
    idle_time_before_scale_down=120,
    tier="Dedicated",
)

cpu_cluster = ml_client.compute.begin_create_or_update(cpu_cluster)