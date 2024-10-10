## Testing external demo Solution Accelerator with access System NIM endpoints

**Prerequisites**

Ensure that the llama3-8b and Rag Coordinator nims installed:
 - Go to "Get Started with Solution Accelerators" interface.
 - Click on `Endpoint Details` (top right corner).

 #TODO: add screenshot with `Endpoint Details` 

**Steps** 

**Import Tar File:**

- Go to "Get Started with Solution Accelerators" interface.
- Click on `Add New`.
- Upload the tar file containing the demo app.
   - demo-app-llm-0.1.2-b12dc34.tar.gz
   - demo-app-rag-0.1.2-b12dc34.tar.gz

  these examples already contain configured `Values.ezua.solutionAccelerators.` section.

**_NOTE:_**  Full list of available Solution Accelerators:
```yaml
ezua:
  solutionAccelerators:
    embedding-v5: ${NV_EMBEDQA_E5_V5_SERVICE_URL}
    embedding-mistral-7b-v2: ${NV_EMBEDQA_MISTRAL_7B_V2_SERVICE_URL}
    llama3-8b: ${LLAMA3_8B_INSTRUCT_SERVICE_URL}
    ragCoordinator: ${RAG_COORDINATOR_URL}
    reranker: ${NV_RERANKQA_MISTRAL_4B_V3_SERVICE_URL}
    vectorStore: ${VECTOR_STORE_URL}
```

**Deploy Application:**

Click the "Deploy" button to start the deployment process.

**Testing**

Verify Deployment:

Ensure the application is deployed successfully and the `Open` button is available.

Get or generate an auth token

- for llm endpoint testing, use service token

```
kubectl create token ext-app3 -n ui --duration 24h
```
 
- for rag coordinator endpoint testing, use the auth token
 
```
kubectl get secrets access-token -n <user_namespace> -o json | jq -r .data.AUTH_TOKEN  | base64 -d
```

Run Tests:

Insert auth_token into `request headers`:
```
"Authorization": "Bearer enter_auth_token_here",
```

Click button `Send Request`.

The output field will contain the response data or error information if one occurred.
