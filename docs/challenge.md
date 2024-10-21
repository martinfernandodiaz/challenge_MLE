# Software Engineer (ML & LLMs) Challenge: documentation and explanations

## Part I

### Model selection: Considerations and comments

- About bussiness:

    Detecting flight delays is key for the bussiness (delay = 1). 

- About imbalanced target:

    I note that the model must be trained taking into account the balance of the target feature (to obtain a consistent recall value).

- About model selection: 

    Both the XGboost model and the Linear Regression model have the same performance, I will select the Linear Regression model for its simplicity of interpretation, since it allows to easily explain to the bussiness how a prediction is made and why some features are more important than others.

## Part III

### Arquitecture used on GCP

The service was deployed on Cloud Run, utilizing Artifact Registry as my Docker repository for the API image, which serves as the source for the Cloud Run service.

I created a service account with the Cloud Run Invoker role to assign this identity to the revisions of the Cloud Run instance.

Additionally, I established another service account for CI/CD purposes, ensuring it has only the minimal roles required (Cloud Run Developer, Artifact Registry Writer and Service Account User).


*Note: The Cloud Run service scales from 0 instances, which means it may take a few seconds to scale up to the maximum of 1 instance when the service receives a request.*


## Part IV

### Consdierations

The version of the Docker image is currently hardcoded for simplicity. An alternative approach would be to use a Commit SHA stored in the GitHub repository environment or to implement a versioning strategy such as Semantic Versioning.

The incorporation of the tests already performed (with Makefile) into the integration pipeline is still pending. However, both the CI and CD pipelines are functional.