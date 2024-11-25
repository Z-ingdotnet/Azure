# hyperparameter search space: 
# batch_size hyperparameter can have the value 16, 32, or 64
# the learning_rate hyperparameter can have any value from a normal distribution with a mean of 10 and a standard deviation of 3



from azure.ai.ml.sweep import Choice, Normal

command_job_for_sweep = job(
    batch_size=Choice(values=[16, 32, 64]),    
    learning_rate=Normal(mu=10, sigma=3),
)