# NVIDIA-NIM Unit Testing Guide

This guide explains how to test NVIDIA-NIM unit tests using the Solution Accelerator.

## Prerequisites

- Access to the Solution Accelerator platform
- Runtime image path and tag for the solution accelerator application
- Cluster access with appropriate permissions

## Setup Process

### 1. Import Tar File
1. Navigate to the "Get Started" section of Solution Accelerator interface
2. Click "Add New"
3. Upload your NVIDIA-NIM unit tests tar file
4. Complete the solution accelerator details
   > **Note**: For non-user namespace deployment, add label `hpe-ezua/ezmodels=true` to the namespace

### 2. Configure Runtime Settings
![nim](https://github.com/user-attachments/assets/e064bf1c-8539-4169-9290-9ea0a7f272cb)

Update the following default values in Solution Accelerator Values:
- ClusterServingRuntime Image Path
- ClusterServingRuntime Image Tag

### 3. Deploy
Click "Deploy" to initiate the deployment process

## Testing Guide

### Deployment Verification
1. Check if the application deployed successfully
2. Verify the inference service is running
3. Obtain the service URL for testing

## API Examples

Replace the following in all URLs:
- `<namespace>`: Your deployment namespace
- `<domain>`: Your cluster domain

### 1. Embedding API

```bash
curl --location "https://embed-e5-v5-predictor-${NAMESPACE}.${DOMAIN}/v1/embeddings" \
--header 'Content-Type: application/json' \
--data '{
    "input": "This is a test query",
    "input_type": "query",
    "model": "nvidia/nv-embedqa-e5-v5"
}'
```

### 2. LLM API

```bash
curl -X POST "https://llama3-8b-predictor-${NAMESPACE}.${DOMAIN}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama3-8b-instruct",
    "messages": [
      {
        "role": "user",
        "content": "Hello! How are you?"
      }
    ],
    "max_tokens": 256,
    "stream": false
  }'
```
