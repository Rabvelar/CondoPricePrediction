import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the CSV file (for reference and display purposes)
df = pd.read_csv("jobs_in_data.csv")

# Function to load the saved model and LabelEncoders
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

# Extracting the regressor and label encoders from the loaded data
regressor_loaded = data["model"]
le_job_title = data["le_job_title"]
le_experience_level = data["le_experience_level"]
le_work_setting = data["le_work_setting"]
le_company_location = data["le_company_location"]

# Function to create the prediction page
def show_predict_page():
    st.title("📊 Data Jobs Salary Prediction App")

    st.info('This app predicts the salary for various data job roles based on input features like job title, experience level, work setting, and company location.')

    st.write("""### We need some information to predict the salary:""")

    # Input selections for the app's sidebar
    job_titles = (
        'Data Analyst',
        'Data Scientist',
        'Data Engineer',
        'Machine Learning Engineer',
        'Data Architect',
        'Analytics Engineer',
        'Applied Scientist',
        'Research Scientist',
    )
    experience_levels = (
        'Entry-level',
        'Mid-level',
        'Senior',
        'Executive',
    )
    work_settings = (
        'Office',
        'Hybrid',
        'Remote',
    )
    company_locations = (
        'United States',
        'United Kingdom',
        'Canada',
        'Spain',
        'Germany',
        'France',
        'Netherlands',
        'Portugal',
        'Australia',
        'Other',
    )

    # Input fields for users to provide data
    job_title = st.selectbox("Job Title", job_titles)
    experience_level = st.selectbox("Experience Level", experience_levels)
    work_setting = st.selectbox("Work Type", work_settings)
    company_location = st.selectbox("Company Location", company_locations)

    # Predict salary when the button is clicked
    if st.button("Calculate Salary"):
        # Input array for the prediction
        x = np.array([[job_title, experience_level, work_setting, company_location]])
        
        # Apply label encoders to the input data
        x[:, 0] = le_job_title.transform(x[:, 0])
        x[:, 1] = le_experience_level.transform(x[:, 1])
        x[:, 2] = le_work_setting.transform(x[:, 2])
        x[:, 3] = le_company_location.transform(x[:, 3])
        x = x.astype(float)

        # Predict salary using the loaded model
        salary = regressor_loaded.predict(x)

        # Display the predicted salary
        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")

show_predict_page()
