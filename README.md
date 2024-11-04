# model-test-run

`model-test-run` service. Used for testing and packing models. Can be wrapped in a Docker container and deployed to Kubernetes.

Key features:

1. **Resolving model YAML files** into Conda environment files and building environments.
2. **Running bioimageio.core** to test models for compatibility.
3. **Creating Conda pack files** after model publication, uploading them to S3.


