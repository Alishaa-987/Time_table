import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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

# App title
st.title("University Timetable and Task Manager")

# Set initial background image
default_bg = "https://www.w3schools.com/w3images/lights.jpg"
set_bg_image(default_bg)

# Background Image Selection
st.sidebar.header("Settings")
bg_image = st.sidebar.selectbox("Choose Background Image", 
                                  ["https://www.w3schools.com/w3images/lights.jpg", 
                                   "https://www.w3schools.com/w3images/fjords.jpg", 
                                   "https://www.w3schools.com/w3images/nature.jpg", 
                                   "https://www.w3schools.com/w3images/mountains.jpg"])
set_bg_image(bg_image)

# Input number of classes
st.header("Enter Your Classes")
num_classes = st.number_input("Number of Classes:", min_value=1, max_value=10, value=1)

# Initialize a session state for storing classes
if 'classes' not in st.session_state:
    st.session_state.classes = []

# Form for adding class details
for i in range(num_classes):
    with st.form(key=f'class_form_{i}'):
        class_name = st.text_input(f"Class Name {i + 1}")
        topics = st.text_area(f"Topics for {class_name} (comma-separated)")
        deadline = st.date_input(f"Assignment Deadline for {class_name}")
        priority = st.selectbox(f"Priority for {class_name}", ["High", "Medium", "Low"])
        
        # Submit button
        submit_button = st.form_submit_button(label="Add Class")
        
        # If user clicks the submit button
        if submit_button:
            if class_name and topics:  # Ensure inputs are not empty
                st.session_state.classes.append({
                    "Class Name": class_name, 
                    "Topics": topics.split(','), 
                    "Deadline": deadline, 
                    "Priority": priority
                })
                st.success(f"Added: {class_name} with topics {topics}")

# Display the timetable if classes have been added
if st.session_state.classes:
    st.header("Your Timetable")
    timetable_df = pd.DataFrame(st.session_state.classes)
    st.dataframe(timetable_df)

    # Calculate suggested times to complete assignments based on deadlines
    st.header("Suggested Times to Complete Assignments")
    for cls in st.session_state.classes:
        deadline = cls["Deadline"]
        today = datetime.now().date()
        remaining_days = (deadline - today).days

        if remaining_days > 0:
            suggested_time = datetime.now() + timedelta(hours=remaining_days * 2)  # Suggesting 2 hours per remaining day
            st.write(f"**{cls['Class Name']}**: Suggested completion time for assignments is {suggested_time.strftime('%Y-%m-%d %H:%M')}.")

# Option to reset the timetable
if st.button("Reset Timetable"):
    st.session_state.classes.clear()
    st.experimental_rerun()
