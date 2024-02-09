import streamlit as st
import cv2

def main():
    st.sidebar.title("Configuration")
    url = st.sidebar.text_input("Enter URL")
    st.write(f"URL: {url}")

    # Load the .pb file
    model = cv2.dnn.readNetFromTensorflow('./end2end.pb')

    # Make predictions
    output = model.forward()

    # Print the predictions
    print(output)


if __name__ == "__main__":
    main()
