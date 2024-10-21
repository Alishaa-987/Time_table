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
        h1, h2, h3 {{
            font-family: 'Courier New', Courier, monospace;  /* Stylish Font */
        }}
        .stTextInput, .stTextArea, .stSelectbox, .stDateInput {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px; /* Rounded boxes */
            padding: 10px;
            font-size: 16px;
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
        class_name = st.text_input(f"Class Name {i + 1}", key=f'class_name_{i}')
        topics = st.text_area(f"Topics for {class_name} (comma-separated)", key=f'topics_{i}')
        deadline = st.date_input(f"Assignment Deadline for {class_name}", key=f'deadline_{i}')
        priority = st.selectbox(f"Priority for {class_name}", ["High", "Medium", "Low"], key=f'priority_{i}')

        # Submit button
        submit_button = st.form_submit_button(label="Add Class")

        # Change color and clear input on submit
        if submit_button:
            if class_name and topics:  # Ensure inputs are not empty
                st.session_state.classes.append({
                    "Class Name": class_name, 
                    "Topics": topics.split(','), 
                    "Deadline": deadline, 
                    "Priority": priority
                })
                st.success(f"Added: {class_name} with topics {topics}")

                # Clear inputs
                st.experimental_rerun()

# Ask for assignments or quizzes
if st.session_state.classes:
    st.header("Additional Tasks")
    for cls in st.session_state.classes:
        with st.expander(cls["Class Name"]):
            has_assignment = st.radio(f"Is there an assignment or quiz for {cls['Class Name']}?", 
                                      ["Yes", "No"], key=f'has_assignment_{cls["Class Name"]}')

            if has_assignment == "Yes":
                assignment_deadline = st.date_input(f"Assignment/Quiz Deadline for {cls['Class Name']}", key=f'assignment_deadline_{cls["Class Name"]}')
                st.session_state.classes[-1]["Assignment Deadline"] = assignment_deadline

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
