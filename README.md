# model-test-run

`model-test-run` automates testing and deployment of models by:

1. **Resolving model YAML files** into Conda environment files and building environments.
2. **Running bioimageio.core** to test models for compatibility and functionality.
3. **Creating Conda pack files** after model publication, uploading them to S3 for deployment.

The project aims to build a Hypha service (`model-test-run`) that provides these functions as a scalable, containerized service, which can be wrapped in a Docker container and deployed to Kubernetes.

## Key Features

- **Model YAML Parsing**: Translates model YAML definitions to Conda environment specs.
- **Environment Management**: Automates Conda environment setup and dependency installation.
- **Model Testing**: Uses bioimageio.core for structured model testing and validation.
- **Pack & Publish**: Packages environments, uploads to S3, and prepares models for scalable deployment.


