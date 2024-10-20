import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Set background color with CSS


# Load the saved CatBoost model
@st.cache_resource
def load_model():
    with open('best_catboost_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Load the model
model = load_model()

# Load the dataset for exploration
@st.cache_data
def load_data():
    df = pd.read_csv("condo_data_final.csv")  # Load your dataset here
    return df

# Load the data
data = load_data()

# Function to create the prediction page
# Function to create the prediction page
def show_predict_page():
    st.title("📊 Condominium Price Prediction")
    st.info('This app predicts the condo price per square meter based on input features.')

    st.write("### Please provide the following details for an accurate price prediction:")

    # First Row: District and Subdistrict
    col1, col2 = st.columns(2)
    with col1:
        district = st.text_input('District (e.g., Khlong Toei)', value='Khlong Toei')
    with col2:
        subdistrict = st.text_input('Subdistrict (e.g., Phra Khanong)', value='Phra Khanong')

    # Second Row: Room Size and BuildingAge
    col3, col4 = st.columns(2)
    with col3:
        total_units = st.number_input('Total Units', min_value=0, value=280)
    with col4:
        built_age = st.number_input('BuildingAge', min_value=0, value=15)

    # Third Section: Room Size Selection
    st.write("### Select Room Size:")
    room_size_option = st.selectbox('Room Size', ['Studio', '1 Bedroom', '2 Bedrooms', '3 Bedrooms'])

    # Define room size in square meters
    room_size_dict = {
        'Studio': 24,
        '1 Bedroom': 30,
        '2 Bedrooms': 55,
        '3 Bedrooms': 80
    }
    room_size_sqm = room_size_dict[room_size_option]  # Get the room size in sqm based on selection

    # Fourth Section: Distances (each slider on a separate row)
    st.write("### Distances to nearby places (in km):")
    train_station = st.slider('Distance to Train Station (km)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    airport = st.slider('Distance to Airport (km)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    university = st.slider('Distance to University (km)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    department_store = st.slider('Distance to Department Store (km)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
    hospital = st.slider('Distance to Hospital (km)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)

    # Fifth Row: Facilities (Checkboxes)
    st.write("### Available Facilities:")
    col5, col6 = st.columns(2)
    with col5:
        car_park = st.checkbox('Car Park', value=True)
        cctv = st.checkbox('CCTV', value=True)
        fitness = st.checkbox('Fitness', value=True)
        swimming_pool = st.checkbox('Swimming Pool', value=True)
    with col6:
        library = st.checkbox('Library', value=False)
        security = st.checkbox('Security', value=True)
        mini_mart = st.checkbox('Mini Mart', value=True)
        electrical_substation = st.checkbox('Electrical Substation', value=True)

    # Prediction button
    if st.button("Predict"):
        # Prepare the input data
        feature_values = [
            train_station,              # TrainStation (Numerical)
            university,                 # University (Numerical)
            airport,                    # Airport (Numerical)
            department_store,           # DepartmentStore (Numerical)
            hospital,                   # Hospital (Numerical)
            str(subdistrict),           # Subdistrict (Categorical)
            str(district),              # District (Categorical)
            total_units,                # TotalUnits (Numerical)
            built_age,                  # BuildingAge (Numerical)
            int(car_park),              # CarPark (Binary)
            int(cctv),                  # CCTV (Binary)
            int(fitness),               # Fitness (Binary)
            int(library),               # Library (Binary)
            int(swimming_pool),         # Swimmingpool (Binary)
            int(security),              # Security (Binary)
            int(mini_mart),             # MiniMart (Binary)
            int(electrical_substation)  # ElectricalSubStation (Binary)
        ]

        # Define the feature names
        feature_names = [
            'TrainStation', 'University', 'Airport', 'Departmentstore', 
            'Hospital', 'Subdistrict', 'District', 'TotalUnits', 
            'BuildingAge',  # Use 'BuildingAge' as the feature name
            'CarPark', 'CCTV', 'Fitness', 
            'Library', 'Swimmingpool', 'Security', 'MiniMart', 
            'ElectricalSubStation'
        ]

        # Convert the feature values into a DataFrame
        feature_array = pd.DataFrame([feature_values], columns=feature_names)

        # Ensure categorical columns are treated as categorical
        feature_array['Subdistrict'] = feature_array['Subdistrict'].astype('category')
        feature_array['District'] = feature_array['District'].astype('category')

        # Make the prediction using the loaded model
        try:
            prediction = model.predict(feature_array)
            predicted_psm = prediction[0]  # Predicted price per square meter
            total_price = predicted_psm * room_size_sqm  # Calculate total price based on room size

            st.subheader(f"The estimated condo price per square meter is: ฿{predicted_psm:,.2f}")
            st.subheader(f"Estimated Total Price for the selected room size ({room_size_sqm} sqm): ฿{total_price:,.2f}")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# Function to create the exploration page
def show_exploration_page():
    st.title("📊 Data Exploration: Price Distribution by District")

    st.write("### Select a District to view the distribution of Price per Square Meter (PSM):")
    
    # Get unique districts for selection
    unique_districts = data['District'].unique()
    selected_district = st.selectbox('Select District', sorted(unique_districts))

    # Filter data for the selected district
    district_data = data[data['District'] == selected_district]

    # Show distribution of PSM if data exists for the selected district
    if not district_data.empty:
        st.subheader(f"Distribution of Price per Square Meter (PSM) in {selected_district}")
        
        # Histogram
        plt.figure(figsize=(10, 5))
        plt.hist(district_data['PSM'], bins=30, color='skyblue', edgecolor='black')
        plt.xlabel('Price per Square Meter (฿)')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of PSM in {selected_district}')
        plt.grid(axis='y')
        st.pyplot(plt)
        plt.clf()  # Clear the current figure

        # Optionally show a box plot
        st.subheader("Box Plot of PSM")
        plt.figure(figsize=(10, 5))
        plt.boxplot(district_data['PSM'], vert=False)
        plt.xlabel('Price per Square Meter (฿)')
        plt.title(f'Box Plot of PSM in {selected_district}')
        st.pyplot(plt)
        plt.clf()  # Clear the current figure
    else:
        st.warning("No data available for the selected district.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Price Prediction", "Data Exploration"])

if page == "Price Prediction":
    show_predict_page()
else:
    show_exploration_page()
