import streamlit as st
import pandas as pd

# Function to set the background image
def set_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image
set_bg_image("https://www.w3schools.com/w3images/lights.jpg")  # Change to your preferred image URL

# App title
st.title("University Timetable")

# Initialize a session state for storing classes
if 'classes' not in st.session_state:
    st.session_state.classes = []

# Input class details
st.header("Enter Your Classes")

# Form for adding classes
with st.form(key='class_form'):
    class_name = st.text_input("Class Name")
    day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    time = st.text_input("Time (e.g., 10:00 AM - 11:00 AM)")

    # Submit button
    submit_button = st.form_submit_button(label="Add Class")
    
    # If user clicks the submit button
    if submit_button:
        if class_name and time:  # Ensure inputs are not empty
            st.session_state.classes.append({"Class Name": class_name, "Day": day, "Time": time})
            st.success(f"Added: {class_name} on {day} at {time}")

# Display the timetable if classes have been added
if st.session_state.classes:
    st.header("Your Timetable")
    timetable_df = pd.DataFrame(st.session_state.classes)
    st.dataframe(timetable_df)

# Option to reset the timetable
if st.button("Reset Timetable"):
    st.session_state.classes.clear()
    st.experimental_rerun()
