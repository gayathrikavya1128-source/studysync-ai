import streamlit as st
import pandas as pd
from datetime import date
with st.sidebar:
    st.header("📚 StudySync AI")
    st.info(
        "Generate smart study plans, "
        "track progress, and stay exam-ready."
    )

st.title("📚 StudySync AI")
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }
    div[data-testid="stMetric"] {
        border: 1px solid #444;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.caption("Smart Study Planner for Students")
st.markdown("---")

st.info(
    "🎯 Personalized study planning with analytics, "
    "timetables, and readiness tracking."
)

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

        days_left = (exam_date - date.today()).days

        st.write(f"📅 Exam Date: {exam_date}")
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

        # Dashboard Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Subjects", len(subject_list))

        with col2:
            st.metric("Study Hours", study_hours)

        with col3:
            st.metric("Days Left", days_left)

        # Table
        st.dataframe(df)

        # Chart
        st.subheader("📊 Study Hours Distribution")
        chart_data = df.set_index("Subject")
        st.bar_chart(chart_data)

        # AI Recommendation
        st.subheader("🤖 AI Study Recommendation")

        if days_left <= 3:
            st.error(
                f"Focus heavily on {priority_subject}. "
                "Your exam is very close."
            )

        elif days_left <= 7:
            st.warning(
                f"Spend extra time on {priority_subject} "
                "and revise daily."
            )

        else:
            st.success(
                f"You have enough time. Maintain consistent study "
                f"for {priority_subject}."
            )

        # Download Button
        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Study Plan",
            data=csv,
            file_name="study_plan.csv",
            mime="text/csv"
        )

        # Daily Timetable
        st.subheader("📅 Daily Study Timetable")

        timetable_days = min(days_left, 7)

        if timetable_days <= 0:
            timetable_days = 1

        for day in range(1, timetable_days + 1):

            st.write(f"### Day {day}")

            for subject in subject_list:

                if subject == priority_subject:
                    hours = round(
                        (study_hours * 0.5),
                        1
                    )
                else:
                    hours = round(
                        (study_hours * 0.5)
                        / max(1, len(subject_list) - 1),
                        1
                    )

                st.write(
                    f"📚 {subject} - {hours} hrs"
                )

            st.divider()

    else:
        st.warning("Please enter at least one subject.")

# Progress Tracker
st.subheader("📈 Study Progress")

progress = st.slider(
    "How much have you completed?",
    0,
    100,
    0
)

st.progress(progress)

st.write(f"{progress}% completed")

st.subheader("🎯 Exam Readiness Score")

readiness_score = progress

if study_hours >= 6:
    readiness_score += 20
elif study_hours >= 4:
    readiness_score += 10

if difficulty == "Hard":
    readiness_score -= 10

readiness_score = max(0, min(readiness_score, 100))

st.metric(
    "Readiness Score",
    f"{readiness_score}/100"
)

if readiness_score >= 80:
    st.success("🟢 You are well prepared!")

elif readiness_score >= 50:
    st.warning("🟡 You need more revision.")

else:
    st.error("🔴 High risk! Increase study effort.")
# Daily Study Tip
st.subheader("💡 Daily Study Tip")

if progress < 25:
    st.info(
        "Start with small study sessions and build momentum."
    )

elif progress < 50:
    st.info(
        "Good progress! Stay consistent and avoid distractions."
    )

elif progress < 75:
    st.success(
        "You're doing well. Focus on revision and practice."
    )

else:
    st.success(
        "Excellent work! Continue revising important topics."
    )

st.divider()

st.success(
    "💪 Small progress every day leads to big success!"
)