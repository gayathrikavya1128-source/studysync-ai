import streamlit as st
from datetime import date

st.title("StudySync AI")

st.write("Welcome to StudySync AI - Smart Study Planner for Students")

name = st.text_input("Enter your name")

if name:
    st.success(f"Welcome, {name}!")

subjects = st.text_area(
    "Enter subjects (one subject per line)"
)

study_hours = st.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=24,
    value=4
)
exam_date = st.date_input("Select Exam Date")
priority_subject = st.selectbox(
    "Select your highest priority subject",
    [s.strip() for s in subjects.split("\n") if s.strip()]
    if subjects.strip()
    else ["No subjects entered"]
)
if st.button("Generate Study Plan"):

    if subjects.strip():

        subject_list = [
            subject.strip()
            for subject in subjects.split("\n")
            if subject.strip()
        ]

        st.write(f"📅 Exam Date: {exam_date}")
        st.subheader("Today's Study Plan")

        remaining_subjects = len(subject_list) - 1

        for subject in subject_list:

            if subject == priority_subject:
                allocated_hours = round(study_hours * 0.5, 1)

            else:
                if remaining_subjects > 0:
                    allocated_hours = round(
                        (study_hours * 0.5) / remaining_subjects,
                        1
                    )
                else:
                    allocated_hours = study_hours

            st.write(f"📚 {subject}: {allocated_hours} hours")

    else:
        st.warning("Please enter at least one subject.")
days_left = (exam_date - date.today()).days

st.write(f"⏳ Days Left Until Exam: {days_left} days")
