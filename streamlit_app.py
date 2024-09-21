import streamlit as st

# Add custom CSS for the bordered box and centering the form
st.markdown(
    """
    <style>
    /* Center the form in the middle of the page */
    .center-form {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    /* Big bordered box for the form */
    .big-box {
        border: 2px solid #e3e3e3;
        border-radius: 15px;
        padding: 30px;
        background-color: #fff;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        width: 400px;
    }

    .center-text {
        text-align: center;
        font-family: 'Arial', sans-serif;
    }

    .predict-button {
        display: flex;
        justify-content: center;
    }

    </style>
    """, unsafe_allow_html=True
)

# Start the centered div
st.markdown('<div class="center-form">', unsafe_allow_html=True)

# Start the bordered box
st.markdown('<div class="big-box">', unsafe_allow_html=True)

# Title
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
st.markdown('<div class="predict-button">', unsafe_allow_html=True)
if st.button('Predict'):
    # Insert prediction logic here
    st.write("Prediction goes here...")  # Placeholder for prediction result
st.markdown('</div>', unsafe_allow_html=True)

# Display prediction result input
price_prediction = st.text_input('', 'THB')

# Close the bordered box and centered form
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
