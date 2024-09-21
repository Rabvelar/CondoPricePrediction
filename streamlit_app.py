import streamlit as st

# Add custom CSS for the bordered box
st.markdown(
    """
    <style>
    .big-box {
        border: 2px solid #d9d9d9;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
    }
    .center-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Start the bordered box
st.markdown('<div class="big-box">', unsafe_allow_html=True)

# Title and Subtitle
st.markdown('<h1 class="center-text">Condo Price Prediction</h1>', unsafe_allow_html=True)

# District Selection
district = st.selectbox('District', ['Bangkhen', 'Chatuchak', 'Ladprao', 'Huai Khwang', 'Wattana'])

# Room Size Selection
room_size = st.selectbox('Room Size', ['Studio', '1 Bedroom', '2 Bedrooms', '3 Bedrooms'])

# Year of Building Input
year_of_building = st.number_input('Year of building', min_value=0, step=1)

# Project Facilities
st.write("Project Facilities")
col1, col2 = st.columns(2)
with col1:
    cctv = st.checkbox('CCTV')
    lift = st.checkbox('Lift')
    fitness = st.checkbox('Fitness')
    swimming_pool = st.checkbox('Swimming Pool')
    shuttle_service = st.checkbox('Shuttle Service')
with col2:
    keycard_access = st.checkbox('Keycard Access Control')
    fingerprint_access = st.checkbox('Fingerprint Access Control')
    convenience_store = st.checkbox('Convenience Store')
    restaurant = st.checkbox('Restaurant')
    bicycle_parking = st.checkbox('Bicycle Parking')

# Predict Button
if st.button('Predict'):
    # Insert prediction logic here, using user input data
    st.write("Prediction goes here...")  # Placeholder for prediction result

# Display prediction result
price_prediction = st.text_input(' ', 'THB')

# Close the bordered box
st.markdown('</div>', unsafe_allow_html=True)
