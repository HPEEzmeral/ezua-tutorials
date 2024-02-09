# Import necessary libraries
import requests
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import streamlit as st
import pandas as pd
import json  # Import the json module
import numpy as np
import boto3
from datetime import datetime

# Define the labels
labels = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum',
           'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'ezmeral coupon',
           'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 
           'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 
           'raddish', 'soy bean', 'spinach', 'sweet potato', 'sweetcorn', 'tomato', 'turnip', 'watermelon']

# Specify the prediction URL. If you are runing this notebook outside of Kubernetes cluster, you should set the Cluster IP.
url = "http://demo-fruit-veg-exp-isvc-predictor-default.demo-user.svc.cluster.local/v1/models/demo-fruit-veg-exp-isvc:predict"

# Set up AWS credentials
AWS_ACCESS_KEY = 'minioadmin'
AWS_SECRET_KEY = 'minioadmin'
BUCKET_NAME = 'ezaf-demo'

S3_ENDPOINT_URL = 'https://minio-console-service.kubeflow.svc.cluster.local:31900'
S3_PATH = 'data/fruit-veg/new/'
S3_DOWNLOADPATH = 'data/fruit-veg/'

# Set up S3 client with ezua credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    endpoint_url=S3_ENDPOINT_URL,
    verify=False  # Disable SSL certificate verification
)

# add logo
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def preprocess_image(image):
    # Resize the image to (224, 224) using PIL's resize function
    image = image.resize((224, 224))

    # Convert the image to a NumPy array using Keras' img_to_array function
    image = img_to_array(image)

    # Expand the dimensions of the image to match the expected shape (1, 224, 224, 3)
    image = np.expand_dims(image, axis=0)

    # Normalize the image by dividing each pixel value by 255.0
    image = image / 255.0

    return image

def format_data(data):
    # Convert the NumPy array to a list using tolist()
    data_list = data.tolist()

    # Format the list as a JSON string using json.dumps()
    data_formatted = json.dumps(data_list)

    # Create a JSON request string with the formatted data
    json_request = '{{ "instances" : {} }}'.format(data_formatted)

    return json_request

# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows, gap="small")
    return grid

def append_row(df, row):
    return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)

def query_presto(product):
    # to be developed this is a quick tweak
    #
    # this is a placeholder for the presto query!
    price=['0.91', '0.27', '1.67', '0.68', '3.28', '1.38',
           '0.98', '2.69', '1.58', '0.65', '0.98', '2.06', '-50%',
           '0.67', '0.90', '4.01', '0.31', '0.56', '0.68', '1.88', '0.88', 
           '0.62', '0.88', '1.32', '1.64', '1.42', '1.84', '1.32', '1.33', 
           '1.28', '2.54', '5.12', '1.33', '1.42', '0.29', '1.48', '6.23']   
    return price[labels.index(product)] 

def upload_file_to_s3(bucket_name, file_path):

    # s3 = boto3.client('s3')
    
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Extract the filename from the file path
    file_name = file_path.split('/')[-1]
    
    # Append the date and time suffix to the filename
    new_file_name = f"{current_datetime}_{file_name}"
    
    try:
        # Upload the file to the S3 bucket
        s3.upload_file(file_path, bucket_name, S3_PATH+ new_file_name)
        print("File uploaded successfully!")
    except Exception as e:
        print(f"Error uploading file: {e}")


def app():
    file_name='data.csv' 
    price = 0

    if "load_state" not in st.session_state:
        st.session_state.load_state = False
        st.session_state['price'] = 0
        df = pd.DataFrame(columns=('Amount', 'Product', 'price'))
        with open(file_name, 'w', encoding='utf-8') as file:
            df.to_csv(file, index=False)
    else:
        with open(file_name, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
        price=st.session_state['price']  

    st.set_page_config(
        page_title="Ezmeral Unified Analytics",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://help.mydirk.de',
            'Report a bug': "https://bug.mydirk.de",
            'About': "Ezmeral Unfied Analytics Demo. Do not hesitate to contact me: dirk.derichsweiler@hpe.com"
        }
    )

    # Hide mainmenu and footer
    #               #MainMenu {visibility: hidden;}
    hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    image=Image.open('hpelogo.png')
    headline = make_grid(1,4)       
    with headline[0][3]:
        st.image(image, width=300)
    with headline[0][0]:
        st.title('HPE Ezmeral Unified Analytics Software')
    st.write('This app is to demonstrate the use of HPE Ezmeral Unified Analytics Software for image classification and is using EzPresto to get the required data fields from the privous created datasets.')
    st.divider()
    grid = make_grid(3,3)
    with grid[0][2]:
        placeholder = st.empty()
        placeholder.data_editor(df, use_container_width=True)
    with grid[2][2]:             
        placeholder_price = st.empty()
        total = df['price'].sum()
        total = "{:.2f}".format(total)
        placeholder_price.title(str("Total: " + str(total) + " USD"))

    st.divider()

    take_photo = grid[0][0].camera_input("live camera feed", label_visibility="collapsed", key="camera-1")

    if take_photo is not None:
        image = Image.open(take_photo)
        grid[0][1].image(image, caption='Uploaded image', use_column_width=True)

        image.convert('RGB')
        image.save('image.jpg', format='JPEG', quality=90)
        
        # Transform image so that it can be sent to the predictor
        preprocessed_image = preprocess_image(image)
        json_request = format_data(preprocessed_image)  # Create JSON request directly

        # Make the POST request to the predictor
        response = requests.post(url, data=json_request)
        response_data = response.json()
        result = response_data['predictions']
        
        formatted_predictions = [[round(pred, 2) for pred in prediction] for prediction in result]
        
        predicted_label_index = np.argmax(result)
        predicted_label = labels[predicted_label_index]

        # st.divider()
        if predicted_label != 'ezmeral coupon':

            st.metric(label="EzPresto Query", value='SELECT price FROM fruits WHERE fruit = "' + predicted_label + '"')
            
            price = query_presto(predicted_label)
            #st.session_state['price']  = st.session_state['price']  + price
            st.metric(label="SQL Return (Value in USD)", value=price)
            
            # Find the index of the last row in the DataFrame
            last_index = df.index.max() + 1 if df.index.max() is not None else 0

            # Update the edited data in the DataFrame
            if "edited_rows" not in st.session_state:
                st.session_state.edited_rows = []
            edited_rows = st.session_state.edited_rows
            if last_index in edited_rows:
                edited_row = edited_rows[last_index]
                for column, edited_value in edited_row.items():
                    df.at[last_index, column] = edited_value            
            # Add a new row if needed
            new_row = pd.Series({'Amount':'1', 'Product':predicted_label, 'price': float(price)})
            if last_index not in edited_rows or len(edited_row) < len(df.columns):
                df = append_row(df, new_row) 
            # Update the CSV file
            with open(file_name, 'w', encoding='utf-8') as file:
                df.to_csv(file, index=False)

            with grid[0][2]:
                placeholder.data_editor(df, use_container_width=True)

            with grid[2][2]: 
                total = df['price'].sum()
                total = "{:.2f}".format(total)
                placeholder_price.title(str("Total: " + str(total) + " USD"))

            upload_file_to_s3(BUCKET_NAME,'image.jpg')

        else:
            st.title("You found the coupon!")
            with grid[2][2]: 
                total_new = float(total) * 0.5
                total_new = "{:.2f}".format(total_new)
                placeholder_price.title(str("reduced price: " + str(total_new) + " USD"))

# Run the app
if __name__ == '__main__':
    app()
