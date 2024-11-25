"""
Steps to create a pipeline:
1. Start with the RAI Insights dashboard constructor.
2. Include one of the RAI tool components.
3. End with Gather RAI Insights dashboard to collect all insights into one dashboard.
4. Optionally, you can also add the Gather RAI Insights score card at the end of your pipeline.


Available tool components and their insights:
- Add Explanation to RAI Insights dashboard:
  Interpret models by generating explanations. Explanations show how much features influence the prediction.

- Add Causal to RAI Insights dashboard:
  Use historical data to view the causal effects of features on outcomes.

- Add Counterfactuals to RAI Insights dashboard:
  Explore how a change in input would change the model's output.

- Add Error Analysis to RAI Insights dashboard:
  Explore the distribution of your data and identify erroneous subgroups of data.
"""



#pipeline with the RAI Insights dashboard constructor component:

rai_constructor_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_insight_constructor", label="latest"
)

#add any of the available insights:

rai_explanation_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_explanation", label="latest"
)

#end pipeline with a Gather RAI Insights dashboard component:
rai_gather_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_insight_gather", label="latest"
)

#build pipeline
from azure.ai.ml import Input, dsl
from azure.ai.ml.constants import AssetTypes

@dsl.pipeline(
    compute="aml-cluster",
    experiment_name="Create RAI Dashboard",
)
def rai_decision_pipeline(
    target_column_name, train_data, test_data
):
    # Initiate the RAIInsights
    create_rai_job = rai_constructor_component(
        title="RAI dashboard diabetes",
        task_type="classification",
        model_info=expected_model_id,
        model_input=Input(type=AssetTypes.MLFLOW_MODEL, path=azureml_model_id),
        train_dataset=train_data,
        test_dataset=test_data,
        target_column_name="Predictions",
    )
    create_rai_job.set_limits(timeout=30)

    # Add explanations
    explanation_job = rai_explanation_component(
        rai_insights_dashboard=create_rai_job.outputs.rai_insights_dashboard,
        comment="add explanation", 
    )
    explanation_job.set_limits(timeout=10)

    # Combine everything
    rai_gather_job = rai_gather_component(
        constructor=create_rai_job.outputs.rai_insights_dashboard,
        insight=explanation_job.outputs.explanation,
    )
    rai_gather_job.set_limits(timeout=10)

    rai_gather_job.outputs.dashboard.mode = "upload"

    return {
        "dashboard": rai_gather_job.outputs.dashboard,
    }

"""
A model is expected to make false predictions, or errors. 
review and understand how errors are distributed in the dataset.

Explore error analysis
Error tree map: explore which combination of subgroups results in the model making more false predictions.
Error heat map: Presents a grid overview of a model's errors over the scale of one or two features.

"""


"""
Explore explanations
Understanding how a model makes predictions is essential for decision-making, especially for complex models. 
To achieve this, model explainers are used to calculate feature importance, which shows how input features influence predictions.

Key Points:

Model Explainers: Tools or techniques to interpret complex models.
Mimic Explainer: A common approach that trains a simple, interpretable model on the same data and task as the complex model.
Feature Importance: Two types can be explored:
Global Feature Importance: Understand overall feature influence across all predictions.
			Aggregate feature importance: Shows how each feature in the test data influences the model's predictions overall.
Local Feature Importance: Examine feature influence for individual predictions.
			Individual feature importance: Shows how each feature impacts an individual prediction.
"""

"""
Explore counterfactuals
Explanations can give insights into the relative importance of features on the model's predictions. 
Sometimes, may want to take it a step further and understand whether the model's predictions would change if the input would be different. 
To explore how the model's output would change based on a change in the input, can use counterfactuals.

can choose to explore counterfactuals what-if examples by selecting a data point and the desired model's prediction for that point. 
When create a what-if counterfactual, the dashboard opens a panel to help  understand which input would result in the desired prediction.

"""



"""
Exploring Causal Analysis

Causal analysis estimates the effect of features on model predictions to improve decision-making and optimize outcomes.

Key Points:
- Purpose: Understand how changes (interventions) in features influence predictions.
- Techniques: Uses statistical methods to estimate average effects for populations or individuals.
- Dashboard Tabs:
  1. Aggregate Causal Effects: Displays average effects of treatment features to optimize predictions.
  2. Individual Causal Effects: Examines how changes in treatment features affect predictions for individual data points.
  3. Treatment Policy: Identifies which data points benefit most from specific treatments.
"""
