# Software Engineer (ML & LLMs) Challenge: documentation and explanations

## Part I

### I.a : Model selection: Considerations and comments

- About bussiness:

    Detecting flight delays is key for the bussiness (delay = 1). 

- About imbalanced target:

    I note that the model must be trained taking into account the balance of the target feature (to obtain a consistent recall value).

- About model selection: 

    Both the XGboost model and the Linear Regression model have the same performance, I will select the Linear Regression model for its simplicity of interpretation, since it allows to easily explain to the bussiness how a prediction is made and why some characteristics are more important than others.