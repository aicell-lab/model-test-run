# model-test-run

`model-test-run` service. Used for testing and packing models. Can be wrapped in a Docker container and deployed to Kubernetes.

Key features:

1. **Resolving model YAML files** into Conda environment files and building environments.
2. **Running bioimageio.core** to test models for compatibility.
3. **Creating Conda pack files** after model publication, uploading them to S3.


# TODO:

## Model Testing
Here are the hypha services for model testing:
- static_test for testing yaml # by the user
- create_conda_env # by the user
- run_model_test # both user and reviewer
- upload_conda_env # for the reviewer
- publish_model # for the reviewer
## Chat
- append_chat_message # write to a chat file for this model and send email
- list_chat_messages
