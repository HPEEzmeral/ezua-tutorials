from ray import serve
from joblib import load
from starlette.requests import Request
import numpy as np

# Deployment for a web service with Ray Serve
# To configure your app in a detailed way, it is sugegsted to use FastAPI
@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 2})
class RentPredictor:
    def __init__(self, model_path: str):
        # Load the trained model
        self.model = load(model_path)
        
    async def __call__(self, request: Request) -> dict:
        # Extract features from the request's JSON body
        json_input = await request.json()
        features = np.array([
            [
                json_input['square_footage'], 
                json_input['bedrooms'], 
                json_input['bathrooms'], 
                json_input['furnished']
            ]
        ])
        # Predict the rent using the loaded model
        predicted_rent = self.model.predict(features)[0]
        return {"predicted_rent": predicted_rent}


# Bind the deployment with the model's file path
rent_predictor_app = RentPredictor.bind(model_path="./rent_prediction_model.joblib")

print("Binding is completed.")
