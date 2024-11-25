#Configure a pipeline job

# change the output mode
pipeline_job.outputs.pipeline_job_transformed_data.mode = "upload"
pipeline_job.outputs.pipeline_job_trained_model.mode = "upload"


#set default compute
# set pipeline level compute
pipeline_job.settings.default_compute = "aml-cluster"

#change the default datastore
# set pipeline level datastore
pipeline_job.settings.default_datastore = "workspaceblobstore"


# submit job to workspace
pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="pipeline_job"
)


#Schedule a pipeline job
#create a time-based schedule using the RecurrenceTrigger class
from azure.ai.ml.entities import RecurrenceTrigger

schedule_name = "run_every_minute"

recurrence_trigger = RecurrenceTrigger(
    frequency="minute",
    interval=1,
)

# use JobSchedule class to associate a schedule to a pipeline job
from azure.ai.ml.entities import JobSchedule

job_schedule = JobSchedule(
    name=schedule_name, trigger=recurrence_trigger, create_job=pipeline_job
)

job_schedule = ml_client.schedules.begin_create_or_update(
    schedule=job_schedule
).result()


#disable schedule
ml_client.schedules.begin_disable(name=schedule_name).result()
ml_client.schedules.begin_delete(name=schedule_name).result()