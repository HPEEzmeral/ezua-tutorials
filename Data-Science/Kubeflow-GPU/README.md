# Running kubeflow-on-gpu example

## Running Kubeflow Notebooks on GPU

In order to create Kubfeflow notebook with GPU, choose corresponding image with CUDA support. During notebook server
creation, click on "Custom Notebook" button within selected "Jupyter" section, and choose one of the following images
in drop-down from the notebook images list:

* `gcr.io/mapr-252711/kubeflow/notebooks/jupyter-tensorflow-cuda-full:<TAG>` (Tensorflow CUDA image)
* `gcr.io/mapr-252711/kubeflow/notebooks/jupyter-pytorch-cuda-full:<TAG>` (PyTorch CUDA image)

Note: `TAG` will vary based on the UA releases.

</br>

Also set number of GPUs to 1 in "GPU" section and select "Nvidia" in "GPU Vendor" drop-down:

![nb-gpu-requests](img/nb-gpu-requests.png)

### Checking GPU availability in Kubeflow Notebook with requested GPU resources

Open `Check_gpu_card.ipynb` notebook and run all cells in order to check GPU availability in Kubeflow Notebook with
Tensorflow CUDA image. If GPU is available, the following output will be displayed:

![check-gpu-nb](img/check_gpu_nb_1.jpg)

![check-gpu-nb](img/check_gpu_nb_2.jpg)

Also for verification purposes, `nvidia-smi` command can be executed in pod of daemonset
`nvidia-device-plugin-daemonset` in `hpecp-gpu-operator` namespace. If python3 process is shown as in the following
image, then GPU is working properly within Kubeflow Notebook:

![check-gpu-nb](img/check_gpu_nb_3.jpg)

## Running InferenceService on GPU for trained model

In order to run inference service on GPU for trained model, create `InferenceService` resource and specify in resources
section `nvidia.com/gpu: 1` as limits. For example:

```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "tensorflow-gpu"
  namespace: "<username>"
spec:
  predictor:
    serviceAccountName: <service-account-name>
    tensorflow:
      storageUri: "<path-to-model>"
      resources:
        limits:
          nvidia.com/gpu: 1
```

### Deploying InferenceService on GPU for trained MNIST model

Open `Train_and_infer_mnist.ipynb` notebook in order to train MNIST model with Tensorflow on GPU and deploy
InferenceService on GPU for trained model. Run all cells in notebook just to check that it works properly. In the last
cell of the notebook there should be a test images with predicted labels - it means that InferenceService is working
properly on GPU.
