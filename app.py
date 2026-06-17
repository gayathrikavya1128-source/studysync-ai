import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 StudySync AI")
st.caption("Smart Study Planner for Students")

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

difficulty = st.selectbox(
    "Select difficulty level",
    ["Easy", "Medium", "Hard"]
)

if difficulty == "Hard":
    study_hours += 2
elif difficulty == "Medium":
    study_hours += 1

if st.button("Generate Study Plan"):

    if subjects.strip():

        subject_list = [
            subject.strip()
            for subject in subjects.split("\n")
            if subject.strip()
        ]

        st.write(f"📅 Exam Date: {exam_date}")

        days_left = (exam_date - date.today()).days

        st.write(f"⏳ Days Left Until Exam: {days_left} days")

        if days_left <= 7:
            st.error("⚠️ Exam is very close! Increase study focus.")

        st.subheader("Today's Study Plan")

        remaining_subjects = len(subject_list) - 1
        plan_data = []

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

            plan_data.append([subject, allocated_hours])

        df = pd.DataFrame(
    plan_data,
    columns=["Subject", "Allocated Hours"]
)

    col1, col2, col3 = st.columns(3)

    with col1:
      st.metric("Subjects", len(subject_list))

    with col2:
      st.metric("Study Hours", study_hours)

    with col3:
      st.metric("Days Left", days_left)

    st.dataframe(df)
    st.subheader("📊 Study Hours Distribution")

    chart_data = df.set_index("Subject")

    st.bar_chart(chart_data)
    csv = df.to_csv(index=False)

    st.download_button(
            label="📥 Download Study Plan",
            data=csv,
            file_name="study_plan.csv",
            mime="text/csv"
        )

else:
    st.warning("Please enter at least one subject.")

st.subheader("Study Progress")

progress = st.slider(
    "How much have you completed?",
    0,
    100,
    0
)

st.progress(progress)

st.write(f"{progress}% completed")

st.divider()

st.success(
    "💪 Small progress every day leads to big success!"
)
