import json
import logging
import requests

import gradio as gr
import gradio.components as components

from theme import EzmeralTheme
from mappings import (customers_map, age_map, gender_map,
                      merchant_map, category_map)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


DOMAIN_NAME = "svc.cluster.local"
NAMESPACE = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r").read()
DEPLOYMENT_NAME = "fraud-detection"
MODEL_NAME = DEPLOYMENT_NAME
SVC = f'{DEPLOYMENT_NAME}-predictor.{NAMESPACE}.{DOMAIN_NAME}'
URL = f"https://{SVC}/v2/models/{MODEL_NAME}/infer"


def detect(step: int, customer: int, age: int, gender: int, merchant: int,
           category: int, amount: float, request: gr.Request):

    customer = customers_map[customer]
    age = age_map[age]
    gender = gender_map[gender]
    merchant = merchant_map[merchant]
    category = category_map[category]
    
    data = [step, customer, age, gender, merchant, category, amount]

    logger.info(f"Sending data: {data}")

    payload = {
        "inputs" : [{
            "name" : "fraud-detection-infer-001",
            "datatype": "FP32",
            "shape": [1, 7],
            "data": [data],
        }]
    }

    headers = {"Authorization": request.headers.get("authorization")}
    response = requests.post(URL, json=payload, headers=headers, verify=False)

    logger.info(f"Response: {response}")
    logger.info(f"Response: {response.text}")

    res =  json.loads(response.__dict__.get('_content')).get('outputs')[0]['data'][0]

    logger.info(f"Response: {res}")

    return "Fraud" if res == 1 else "Not Fraud"


if __name__ == "__main__":
    customer_dropdown = [
    "C1053477622",
    "C1055224400",
    "C1155259690",
    "C1332295774",
    "C1450140987",
    "C1619755203",
    "C1697851479",
    "C1769470125",
    "C1814870538",
    "C1881708420",
    "C1952040134",
    "C2055009466",
    "C2072009750",
    "C545248492",
    "C583110837",
    "C603564532",
    "C77415586",
    "C778323844",
    "C986156699"
]

merchant_dropdown = [
    "M1823072687",
    "M348934600",
    "M480131234",
    "M480139044",
    "M980657600"
]

category_dropdown = ["Health", "Sports and Toys", "Transportation"]

gender_dropdown = ["Enterprise", "Female", "Male", "Unknown"]

age_dropdown = [
    "<= 18 years",
    "19-25 years",
    "26-35 years",
    "36-45 years",
    "46-55 years",
    "56-65 years",
    "> 65 years",
    "Unknown"
]

interface = gr.Interface(
    description='<img src="file/app-banner.png" alt="fraud-detection" style="width:100%; height:auto;">',
    fn=detect,
    inputs=[
        components.Number(
            label="Day of the Year", minimum=1, maximum=365, value=1),
        components.Dropdown(choices=customer_dropdown, label="Customer"),
        components.Dropdown(choices=age_dropdown, label="Age"),
        components.Dropdown(choices=gender_dropdown, label="Gender"),
        components.Dropdown(choices=merchant_dropdown, label="Merchant"),
        components.Dropdown(choices=category_dropdown, label="Category"),
        components.Number(label="Amount"),
    ],
    outputs=components.Textbox(),
    theme=EzmeralTheme()
)

interface.launch(server_name="0.0.0.0", server_port=8080)
