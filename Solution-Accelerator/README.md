# NVIDIA-NIM Unit Tests with Solution Accelerator

This guide explains how to test NVIDIA-NIM unit tests using the Solution Accelerator.

## Prerequisites

- Access to the Solution Accelerator platform
- Runtime image path and tag for the solution accelerator application
- Cluster access with appropriate permissions

## Setup Process

### 1. Import Tar File
1. Navigate to the Tools & Framework section
2. Click "Import Framework"
3. Upload your helm charts unit tests tar file (They can we found in ezua-tutorials/Solution-Accelerator/helm-package) 
4. Complete the solution accelerator details
   > **Note**: For non-user namespace deployment, add label `hpe-ezua/ezmodels=true` to the namespace

### 2. Configure Runtime Settings
![nim](https://github.com/user-attachments/assets/e064bf1c-8539-4169-9290-9ea0a7f272cb)

Update the following default values in Solution Accelerator Values:
- ClusterServingRuntime Image Path
- ClusterServingRuntime Image Tag

### 3. Deploy
Click "Deploy" to initiate the deployment process

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
### 2. llama 3.1 8b API

```bash
curl -X POST "https://llama3-1-8b-predictor-${NAMESPACE}.${DOMAIN}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
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

### 3. llama 3 8b API

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

### 4. Reranker API
```bash
curl --location "https://nv-rerankqa-mistral-4b-v3-predictor-${NAMESPACE}.${DOMAIN}/v1/ranking" \
--header 'Content-Type: application/json' \
--data '{
  "model": "nvidia/nv-rerankqa-mistral-4b-v3",
  "query": {
    "text": "What is the GPU memory bandwidth of H100 SXM?"
  },
  "passages": [
    {
      "text": "The Hopper GPU is paired with the Grace CPU using NVIDIA'\''s ultra-fast chip-to-chip interconnect, delivering 900GB/s of bandwidth, 7X faster than PCIe Gen5. This innovative design will deliver up to 30X higher aggregate system memory bandwidth to the GPU compared to today'\''s fastest servers and up to 10X higher performance for applications running terabytes of data."
    },
    {
      "text": "A100 provides up to 20X higher performance over the prior generation and can be partitioned into seven GPU instances to dynamically adjust to shifting demands. The A100 80GB debuts the world'\''s fastest memory bandwidth at over 2 terabytes per second (TB/s) to run the largest models and datasets."
    },
    {
      "text": "Accelerated servers with H100 deliver the compute power—along with 3 terabytes per second (TB/s) of memory bandwidth per GPU and scalability with NVLink and NVSwitch™."
    }
  ]
}'
