import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle


## Load the Trained model
model = tf.keras.models.load_model("model.h5")

## load the encoder and scaler
with open("OneHot_encoder_geo.pkl", "rb") as file:
    OHE_encoder = pickle.load(file)

with open("Label_encoder_gender.pkl", "rb") as file:
    label_encoder = pickle.load(file)

with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

## Streamlit app
st.title("Customer Churn Prediction")


# User input
geography = st.selectbox('Geography', OHE_encoder.categories_[0])
gender = st.selectbox('Gender', label_encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})


# One-hot encode 'Geography'
geo_encoded = OHE_encoder.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=OHE_encoder.get_feature_names_out(['Geography']))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale the input data
input_data_scaled = scaler.transform(input_data)

if st.button("🔎 Predict Customer Churn Or Not"):
# Predict churn
    prediction = model.predict(input_data_scaled)
    prediction_proba = prediction[0][0]
    result = "🛑 The customer is likely to churn." if prediction_proba > 0.5 else "✅ The customer is not likely to churn."
    st.success(f"**Prediction:** {result}")
    st.success(f"**Churn Probability::** {prediction_proba:.2f}")
