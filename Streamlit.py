import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Customize Matplotlib style
plt.style.use('dark_background')
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

# Load and process data for exploration
@st.cache_data
def load_data():
    df = pd.read_csv("condo_data.csv")

    # Drop unnecessary columns (if any)
    df.drop(['ID', 'Name','BuildingAge'], axis=1, inplace=True, errors='ignore')

    # Rename target column
    df.rename(columns={'PricePerSquareMeter': 'PSM'}, inplace=True)

    return df

# Load the CSV file for reference
df = load_data()

# Load the model with caching
@st.cache_resource
def load_model():
    with open('./saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

# Extract the regressor
regressor_loaded = data["model"]

# Function to create the prediction page
def show_predict_page():
    st.title("📊 Condominium Price Prediction")
    st.info('This app predicts the condo price based on input features.')

    st.write("### We need some information to predict the condo price:")

    # Dynamically load Districts from the dataset for the search box
    districts = df['District'].unique().tolist()
    selected_district = st.selectbox('Search for District', sorted(districts))

    # Room Size selection
    room_sizes = ('Studio', '1 Bedroom', '2 Bedrooms', '3 Bedrooms')
    selected_room_size = st.selectbox('Room Size', room_sizes)

    # Year of building input
    #year_of_building = st.number_input('Year of building', min_value=1970, max_value=2024, step=1)

    # Distance inputs (in km)
    distances = {
        'TrainStation': st.slider('Distance to Train Station (km)', 0.0, 50.0, step=0.1),
        'University': st.slider('Distance to University (km)', 0.0, 50.0, step=0.1),
        'Airport': st.slider('Distance to Airport (km)', 0.0, 50.0, step=0.1),
        'DepartmentStore': st.slider('Distance to Department Store (km)', 0.0, 50.0, step=0.1),
        'Hospital': st.slider('Distance to Hospital (km)', 0.0, 50.0, step=0.1)
    }

    st.write("### Select available facilities in the condo:")
    col1, col2 = st.columns(2)
    with col1:
        cctv = st.checkbox('CCTV')
        car_park = st.checkbox('Car Park')
        fitness = st.checkbox('Fitness')
        swimming_pool = st.checkbox('Swimming Pool')
    with col2:
        security = st.checkbox('Security')
        library = st.checkbox('Library')
        mini_mart = st.checkbox('Mini Mart')
        electrical_substation = st.checkbox('Electrical Substation')

    # Prediction button
    if st.button("Predict"):
        # Prepare the input data
        input_data = np.array([ 
                                 distances['TrainStation'], 
                                 distances['University'], 
                                 distances['Airport'],
                                 distances['DepartmentStore'], 
                                 distances['Hospital'], 
                                 car_park, 
                                 cctv, 
                                 fitness, 
                                 swimming_pool,
                                 security, 
                                 library, 
                                 mini_mart, 
                                 electrical_substation])

        # Create a DataFrame to include numeric features
        input_df = pd.DataFrame(input_data, columns=[
                                                     'TrainStation', 
                                                     'University', 
                                                     'Airport', 
                                                     'DepartmentStore', 
                                                     'Hospital', 
                                                     'Car Park', 
                                                     'CCTV', 
                                                     'Fitness', 
                                                     'SwimmingPool', 
                                                     'Security', 
                                                     'Library', 
                                                     'MiniMart', 
                                                     'ElectricalSubStation'])

        # Calculate BuildingAge
        #current_year = 2024  # or use a dynamic way to get the current year
        #input_df['BuildingAge'] = current_year - input_df['BuiltYear'].astype(int)

        # Add categorical features to the input DataFrame
        input_df['District'] = selected_district
        input_df['RoomSize'] = selected_room_size

        # Ensure the input DataFrame has correct types
        #input_df['BuildingAge'] = input_df['BuildingAge'].astype(int)  # Ensure BuildingAge is int

        # Specify the categorical features for CatBoost
        categorical_features = ['District', 'RoomSize']  # Specify your actual categorical features here
        input_df[categorical_features] = input_df[categorical_features].astype(str)  # Convert categorical features to string

        # Predict using the loaded CatBoost model
        price_prediction = regressor_loaded.predict(input_df)
        st.subheader(f"The estimated condo price per square meter is: ฿{price_prediction[0]:,.2f}")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Price Prediction", "Data Exploration"])

if page == "Price Prediction":
    show_predict_page()
else:
    st.write("Data exploration page not yet implemented.")
