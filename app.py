import streamlit as st
import pandas as pd
import pickle

# Set page configuration
st.set_page_config(
    page_title="Delhi House Price Prediction",  # This changes the browser tab name
    page_icon="🏡"  # You can use emojis or a link to an icon
)

# Load the trained model
model = pickle.load(open("build.pkl", 'rb'))

# Load the label encoders for categorical columns
label_encoders = pickle.load(open("label_encoders.pkl", 'rb'))

# App title
st.title("Delhi House Price Prediction")
st.write("Predict the resale value of houses in Delhi based on their features.")

# Sidebar for user inputs
st.sidebar.header("Enter House Details")

# Input for numerical columns
area = st.sidebar.number_input("Area (in sq. ft)", min_value=0, step=10, value=1000)
bhk = st.sidebar.number_input("Number of BHKs", min_value=1, step=1, value=2)
bathroom = st.sidebar.number_input("Number of Bathrooms", min_value=1, step=1, value=2)
parking = st.sidebar.number_input("Number of Parking Spaces", min_value=0, step=1, value=1)
area_yards = st.sidebar.number_input("Area (in sq. yards)", min_value=0, step=1, value=100)

# Collecting inputs for categorical columns
categorical_columns = ['Furnishing', 'Locality', 'Status', 'Transaction', 'Type']
categorical_inputs = {}
for col in categorical_columns:
    options = label_encoders[col].classes_  # Get unique classes for the column
    categorical_inputs[col] = st.sidebar.selectbox(f"Select {col}", options)

# Transform the categorical inputs using label encoders
encoded_inputs = {}
for col, value in categorical_inputs.items():
    encoded_inputs[col] = label_encoders[col].transform([value])[0]

# Create input DataFrame for prediction in the specified column order
input_data = {
    'Area': [area],
    'BHK': [bhk],
    'Bathroom': [bathroom],
    'Furnishing': [encoded_inputs['Furnishing']],
    'Locality': [encoded_inputs['Locality']],
    'Parking': [parking],
    'Status': [encoded_inputs['Status']],
    'Transaction': [encoded_inputs['Transaction']],
    'Type': [encoded_inputs['Type']],
    'Area_Yards': [area_yards]
}

input_df = pd.DataFrame(input_data)

# Predict and display the result
if st.sidebar.button("Predict Price"):
    prediction = model.predict(input_df)[0]*10**9
    st.success(f"The predicted resale price is ₹{prediction:,.2f}")
