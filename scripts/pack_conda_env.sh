#!/bin/bash

# Check if environment file is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 environment.yml conda_pack_output.tar.gz"
    exit 1
fi

ENV_YAML="$1"
OUTPUT_FILE="$2"
ENV_NAME=$(basename "$OUTPUT_FILE" .tar.gz)

echo -e "\n"
echo "ENV_YAML=$ENV_YAML" 
echo "OUTPUT_FILE=$OUTPUT_FILE"
echo "ENV_NAME=$ENV_NAME"
echo -e "\n"

echo "Checking for existing environment named $ENV_NAME..."
if conda env list | grep -q "$ENV_NAME"; then
    echo "Environment $ENV_NAME exists. Removing it..."
    yes | conda env remove -n "$ENV_NAME"
fi

echo "Creating temporary conda environment named $ENV_NAME..."
conda env create -f "$ENV_YAML" -n "$ENV_NAME"

if [ $? -ne 0 ]; then
    echo "Failed to create the conda environment."
    exit 1
fi

echo "Activating the temporary environment..."
source activate "$ENV_NAME"
echo "Packing the environment into $OUTPUT_FILE..."
conda-pack -n "$ENV_NAME" -o "$OUTPUT_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to pack the conda environment."
    exit 1
fi

echo "Deactivating the environment..."
source deactivate
echo "Removing the temporary conda environment..."
yes | conda env remove -n "$ENV_NAME"
echo "Environment packed into $OUTPUT_FILE and removed successfully."
