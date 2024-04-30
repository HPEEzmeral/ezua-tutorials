FROM nvcr.io/nvidia/tritonserver:24.03-vllm-python-py3

RUN pip install --upgrade huggingface-hub

COPY model.py /opt/tritonserver/backends/vllm/model.py
