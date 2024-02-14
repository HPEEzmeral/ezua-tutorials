import torch
import numpy as np
import triton_python_backend_utils as pb_utils

from transformers import AutoModel, AutoTokenizer


class TritonPythonModel:
    def initialize(self, args):
        self.tokenizer = AutoTokenizer.from_pretrained("/mnt/models/bge/1/bge-m3", local_files_only=True)
        self.model = AutoModel.from_pretrained("/mnt/models/bge/1/bge-m3", local_files_only=True)

    def execute(self, requests):
        responses = []
        for request in requests:
            inp = pb_utils.get_input_tensor_by_name(request, "text_input")

            byte_data = inp.as_numpy().tolist()[0][0]

            # Decoding the byte data to a string
            decoded_string = byte_data.decode('utf-8')

            tokens = self.tokenizer([decoded_string], padding=True, truncation=True, return_tensors="pt")

            with torch.no_grad():
                output = self.model(**tokens, output_hidden_states=True, return_dict=True)
            
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[
                    pb_utils.Tensor(
                        "embeddings", output.pooler_output.detach().numpy()
                    )
                ]
            )
            responses.append(inference_response)

        return responses
