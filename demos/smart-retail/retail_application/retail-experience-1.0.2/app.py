from flask import Flask, render_template, request, jsonify, request
import os
import base64
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from io import StringIO
from PIL import Image
import json
import logging
import requests
from sqlalchemy import create_engine, text


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Create a file handler and set its level to DEBUG
log_file_path = "app_log.txt"
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


DOMAIN_NAME = "svc.cluster.local"
try:
    NAMESPACE = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r").read() 
except:
    NAMESPACE = 'ezmeral'
    logger.warning("Namespace not found.")
DEPLOYMENT_NAME = "retail-experiment"
MODEL_NAME = DEPLOYMENT_NAME
SVC = f'{DEPLOYMENT_NAME}-predictor.{NAMESPACE}.{DOMAIN_NAME}'
URL = f"http://{SVC}/v1/models/{MODEL_NAME}:predict"


app = Flask(__name__)

def preprocess_image(img):

    img = img.resize((224, 224))
    print(type(img))
    img_array = img_to_array(img)
    print(img_array.shape)
    print(type(img_array))
    img_array = img_array / 255.0
    print(img_array.shape)
    print(type(img_array))
    img_array = np.expand_dims(img_array, axis=0)
    print(img_array.shape)
    print(type(img_array))

    return img_array

def format_data(data):
    # Convert the NumPy array to a list
    data_list = data.tolist()
    
    # Format the list as a JSON string
    data_formatted = json.dumps(data_list)
    
    # Create a JSON request string with the formatted data
    json_request = '{{ "instances" : {} }}'.format(data_formatted)
    
    return json_request


def query_presto(product, engine, country):
    table_name = 'retail.default.' + country
    # This function retrieves the unit price of a product from a Presto database.
    # It uses Keycloak for authentication to obtain an access token, which is then used to create a session
    # for executing the SQL query. The SQL query retrieves the unit price of the specified product from the
    # specified table in the Presto database.
    
    # Update the auth token using the access token obtained from Keycloak
    # auth_token = get_access_and_refresh_tokens(model_user, model_password, keycloak_uri)

    # Define the SQL query to retrieve the unit price of the specified product from the specified table
    QUERY = f"SELECT unitprice FROM {table_name} WHERE PRODUCT = '{product}' LIMIT 1"

    # Execute the SQL query and retrieve the result
    try:
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(text(QUERY))
                logger.warning(result)
                for row in result:
                    # Extract the unit price (a number) from the query result
                    number = float(row[0])
    except Exception as e:
        number = float(5)
        logging.error('Error at %s', 'division', exc_info=e)
                    
    # Return the extracted unit price
    return number

# def detect(image_data):
#     # Placeholder detection function
#     # You can replace this with your actual object detection logic
#     detected_items = ["banana", "apple", "orange"]
#     # Simulate detection by randomly choosing an item from the list
#     detected_item = detected_items[0]  # Placeholder for actual detection logic
#     return detected_item

def detect(image, country):
    try:
        data = format_data(image)

        headers = {"Authorization": request.headers.get("authorization")}
        # Make the POST request
        response = requests.post(URL, data=data, headers=headers, verify=False)

        session = requests.Session()
        session.headers.update(headers)

        logger.warning(response.text)
        logger.warning(response.content.decode('utf-8'))

        response_data = response.json()
        predictions = response_data['predictions']
        formatted_predictions = [[round(pred * 100, 2) for pred in prediction] for prediction in predictions]
        formatted_predictions = formatted_predictions[0]
        logger.warning(formatted_predictions)
        labels = {'apple': 0, 'banana': 1, 'carrot': 2, 'cucumber': 3, 'lemon': 4, 'orange': 5}
        labels = dict((v, k) for k, v in labels.items())

        # Get the predicted label
        predicted_label_index = np.argmax(formatted_predictions)
        logger.warning(predicted_label_index)
        logger.warning(formatted_predictions[predicted_label_index])
        if formatted_predictions[predicted_label_index] > 78:
            predicted_label = labels[predicted_label_index]
            # # Create a SQLAlchemy engine to connect to the Presto database
            engine = create_engine(
                "presto://ezpresto-sts-mst-0.ezpresto-svc-hdl.ezpresto.svc.cluster.local:8081",
                connect_args={
                    "protocol": "https",
                    "requests_kwargs": {"verify": False},
                    "requests_session": session,
                },
            )
            logger.warning(formatted_predictions[predicted_label_index])
            logger.warning(predicted_label)
            price = query_presto(predicted_label, engine, country)
            logger.warning(price)
        else:
            predicted_label = ""
            price = ""
    except:
        predicted_label = ""
        price = ""

    return predicted_label, price 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_frame', methods=['POST'])
def save_frame():
    image_data = request.form['image_data']
    image_bytes = base64.b64decode(image_data.split(',')[1])

    print(type(image_bytes))
    # Save the image to a local JPG file
    image_path = 'frame.jpg'
    with open(image_path, 'wb') as f:
        f.write(image_bytes)

    img = Image.open(image_path)
    image_array = preprocess_image(img)

    logging.warning(URL)
    # Placeholder detect() function to simulate object detection
    country = request.form['country']
    detected_item, item_price = detect(image_array, country)
    if detected_item:
        return jsonify({'item': detected_item.capitalize(), 'price': item_price})
    else:
        return jsonify({'error': 'Error retrieving detection or pricing data'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')