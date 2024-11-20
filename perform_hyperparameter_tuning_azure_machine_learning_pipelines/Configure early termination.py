#use a bandit policy to stop a trial if the target performance metric underperforms the best trial so far by a specified margin.

from azure.ai.ml.sweep import BanditPolicy

sweep_job.early_termination = BanditPolicy(
    slack_amount = 0.2,  # allows an absolute slack amount of 0.2
    delay_evaluation = 5, #with a delay of five trials
    evaluation_interval = 1 #evaluates the policy at every interval
)




#abandons trials where the target performance metric is worse than the median of the running averages for all trials.
from azure.ai.ml.sweep import MedianStoppingPolicy

sweep_job.early_termination = MedianStoppingPolicy(
    delay_evaluation = 5, #with a delay of five trials
    evaluation_interval = 1 #evaluates the policy at every interval
)


# cancels the lowest performing X% of trials at each evaluation interval based on the truncation_percentage value you specify for X.

from azure.ai.ml.sweep import TruncationSelectionPolicy

sweep_job.early_termination = TruncationSelectionPolicy(
    evaluation_interval=1, #evaluates the policy at every interval
    truncation_percentage=20,  #uses a truncation percentage of 20%.
    delay_evaluation=4 #a delay of four trials
)
