import streamlit as st

st.title("StudySync AI")

name = st.text_input("Enter your name")

subjects = st.text_area(
    "Enter subjects (one per line)"
)

study_hours = st.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=24,
    value=4
)

if st.button("Generate Study Plan"):
    st.success("Study plan generation started!")