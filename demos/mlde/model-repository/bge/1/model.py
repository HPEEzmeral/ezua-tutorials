import os
import torch
import logging
import triton_python_backend_utils as pb_utils

from transformers import AutoModel, AutoTokenizer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TritonPythonModel:
    def initialize(self, args):
        model_repository = args.get("model_repository", None)
        if not model_repository:
            logger.warning("Model repository not found in args."
                           " Using default path: `/mnt/models`")
            model_repository = "/mnt/models"
        
        model_version = args.get("model_version", None)
        if not model_version:
            logger.warning("Model version not found in args."
                           " Using default version: `1`")
            model_version = "1"
        
        model_name = args.get("model_name", None)
        if not model_name:
            logger.warning("Model name not found in args."
                           " Using default model: `bge`")
            model_name = "bge"

        model_path = os.path.join(
            model_repository, model_name, model_version, "bge-m3")
        
        logger.info(f"Loading model from: {model_path}...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path, local_files_only=True)
            self.model = AutoModel.from_pretrained(
                model_path, local_files_only=True)
        except OSError as e:
            logger.error(f"Failed to load model from {model_path}. {e}")
            raise
        
        logger.info("Model loaded successfully.")

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
