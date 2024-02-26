import torch
from transformers import AutoModel, AutoTokenizer


class EmbeddingsModel:
    def __init__(self, model_path: str = "bge-m3"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
        self.model.eval()
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model.to(self.device)
        
    def __call__(self, texts):
        return self.embed_documents(texts)
    
    def embed_query(self, query):
        return self.embed_documents(query)[0]

    def embed_documents(self, texts):
        batch_tokens = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        
        batch_tokens.to(self.device)
        
        # Get the embeddings
        with torch.no_grad():
            # Get hidden state of shape [bs, seq_len, hid_dim]
            output = self.model(**batch_tokens, output_hidden_states=True, return_dict=True)

        return output.pooler_output.detach().cpu().numpy().tolist()
