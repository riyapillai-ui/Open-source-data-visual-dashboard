from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "student_performance.csv"
CODE_LABELS = {
    "Gender": {0: "Male", 1: "Female"},
    "Ethnicity": {
        0: "Caucasian",
        1: "African American",
        2: "Asian",
        3: "Other",
    },
    "ParentalEducation": {
        0: "None",
        1: "High School",
        2: "Some College",
        3: "Bachelor's",
        4: "Higher",
    },
    "Tutoring": {0: "No", 1: "Yes"},
    "ParentalSupport": {
        0: "None",
        1: "Low",
        2: "Moderate",
        3: "High",
        4: "Very High",
    },
    "Extracurricular": {0: "No", 1: "Yes"},
    "Sports": {0: "No", 1: "Yes"},
    "Music": {0: "No", 1: "Yes"},
    "Volunteering": {0: "No", 1: "Yes"},
    "GradeClass": {0: "A", 1: "B", 2: "C", 3: "D", 4: "F"},
}

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean the local student-performance CSV."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Add a CSV to the data folder."
        )

    frame = pd.read_csv(DATA_PATH)
    frame = frame.drop_duplicates().dropna(how="all").copy()

    numeric_columns = frame.select_dtypes(include="number").columns
    for column in numeric_columns:
        frame[column] = frame[column].fillna(frame[column].median())

    for column, labels in CODE_LABELS.items():
        if column in frame.columns:
            frame[column] = frame[column].map(labels).fillna(frame[column].astype(str))

    return frame


def numeric_column(frame: pd.DataFrame, *names: str) -> str | None:
    """Return the first available column from a list of expected names."""
    normalized = {column.lower().replace("_", ""): column for column in frame.columns}
    for name in names:
        match = normalized.get(name.lower().replace("_", ""))
        if match is not None:
            return match
    return None


def category_columns(frame: pd.DataFrame) -> list[str]:
    return frame.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


try:
    df = load_data()
except (FileNotFoundError, pd.errors.EmptyDataError) as error:
    st.error(str(error))
    st.stop()

st.markdown(
    """
    <style>
    .main { background: #f7f9fc; }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5eaf2;
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 2px 8px rgba(21, 42, 75, 0.04);
    }
    .dashboard-kicker {
        color: #3366cc;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: -0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="dashboard-kicker">Education · Open-source analysis</div>', unsafe_allow_html=True)
st.title("Student Performance Analysis Dashboard")
st.write(
    "Explore how study habits, absences, and student characteristics "
    "relate to academic performance."
)

categorical_columns = category_columns(df)
with st.sidebar:
    st.header("Explore the data")
    st.caption("Use the filters to compare different student groups.")
    filtered_df = df.copy()
    for column in categorical_columns:
        options = sorted(filtered_df[column].dropna().unique().tolist(), key=str)
        selected = st.multiselect(
            column.replace("_", " "),
            options,
            default=options,
            key=f"filter_{column}",
        )
        filtered_df = filtered_df[filtered_df[column].isin(selected)]

    st.divider()
    st.caption(
        "Data is cleaned by removing duplicates, dropping empty rows, "
        "and filling missing numeric values with medians."
    )

gpa_column = numeric_column(df, "GPA", "Grade")
attendance_column = numeric_column(df, "Attendance", "AttendanceRate", "Absences")
study_column = numeric_column(df, "StudyTimeWeekly", "StudyTime", "WeeklyStudyTime")
attendance_label = (
    "Average absences"
    if attendance_column == "Absences"
    else "Average attendance"
)

if filtered_df.empty:
    st.warning("No students match the selected filters. Adjust the sidebar filters to continue.")
    st.stop()

metric_columns = st.columns(4)
metric_columns[0].metric("Students", f"{len(filtered_df):,}")
metric_columns[1].metric("Average GPA", f"{filtered_df[gpa_column].mean():.2f}" if gpa_column else "—")
metric_columns[2].metric(
    attendance_label,
    f"{filtered_df[attendance_column].mean():.1f}" if attendance_column else "—",
)
metric_columns[3].metric(
    "Avg. weekly study",
    f"{filtered_df[study_column].mean():.1f}" if study_column else "—",
)

st.divider()

grade_column = "GradeClass" if "GradeClass" in filtered_df.columns else None
comparison_columns = [
    column for column in categorical_columns if column not in {grade_column, "StudentID"}
]

overview_tab, factors_tab = st.tabs(["Overview", "Relationships"])

with overview_tab:
    st.subheader("Academic outcomes at a glance")
    st.caption("The donut shows the selected students' grade mix; the line shows how GPA changes across study-time bands.")
    chart_left, chart_right = st.columns(2, gap="large")

    with chart_left:
        if grade_column:
            grade_summary = (
                filtered_df[grade_column]
                .value_counts()
                .rename_axis("Grade")
                .reset_index(name="Students")
            )
            fig_grades = px.pie(
                grade_summary,
                names="Grade",
                values="Students",
                hole=0.55,
                title="Grade distribution",
                color_discrete_sequence=["#1d4ed8", "#3b82f6", "#60a5fa", "#93c5fd", "#dbeafe"],
                template="plotly_white",
            )
            fig_grades.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_grades, width="stretch")
        else:
            st.info("A GradeClass column is required for the grade distribution.")

    with chart_right:
        if study_column and gpa_column:
            study_bands = pd.cut(
                filtered_df[study_column],
                bins=[-float("inf"), 5, 10, 15, 20, 25, float("inf")],
                labels=["0–5 hrs", "5–10 hrs", "10–15 hrs", "15–20 hrs", "20–25 hrs", "25+ hrs"],
            )
            study_summary = (
                filtered_df.assign(StudyBand=study_bands)
                .groupby("StudyBand", observed=True)[gpa_column]
                .mean()
                .reset_index()
            )
            fig_study = px.line(
                study_summary,
                x="StudyBand",
                y=gpa_column,
                markers=True,
                title="Average GPA by weekly study time",
                labels={"StudyBand": "Weekly study time", gpa_column: "Average GPA"},
                color_discrete_sequence=["#3366cc"],
                template="plotly_white",
            )
            fig_study.update_yaxes(range=[0, 4])
            st.plotly_chart(fig_study, width="stretch")
        else:
            st.info("This chart needs numeric StudyTimeWeekly and GPA columns.")

with factors_tab:
    st.subheader("Factors related to academic performance")
    st.caption("Compare GPA across absence bands and the student characteristic that matters most to your question.")
    chart_left, chart_right = st.columns(2, gap="large")

    with chart_left:
        if attendance_column and gpa_column:
            absence_bands = pd.cut(
                filtered_df[attendance_column],
                bins=[-float("inf"), 5, 10, 15, 20, 25, float("inf")],
                labels=["0–5", "6–10", "11–15", "16–20", "21–25", "26+"],
            )
            absence_summary = (
                filtered_df.assign(AbsenceBand=absence_bands)
                .groupby("AbsenceBand", observed=True)[gpa_column]
                .mean()
                .reset_index()
            )
            fig_absences = px.line(
                absence_summary,
                x="AbsenceBand",
                y=gpa_column,
                markers=True,
                title="Average GPA by absences",
                labels={"AbsenceBand": "Absences", gpa_column: "Average GPA"},
                color_discrete_sequence=["#0f766e"],
                template="plotly_white",
            )
            fig_absences.update_yaxes(range=[0, 4])
            st.plotly_chart(fig_absences, width="stretch")
        else:
            st.info("This chart needs numeric Absences and GPA columns.")

    with chart_right:
        if gpa_column and comparison_columns:
            selected_group = st.selectbox(
                "Compare GPA by",
                comparison_columns,
                format_func=lambda value: value.replace("_", " "),
            )
            comparison_summary = (
                filtered_df.groupby(selected_group, dropna=False)[gpa_column]
                .mean()
                .reset_index()
                .sort_values(gpa_column, ascending=False)
            )
            fig_grouped = px.bar(
                comparison_summary,
                x=selected_group,
                y=gpa_column,
                text_auto=".2f",
                title=f"Average GPA by {selected_group.replace('_', ' ')}",
                labels={selected_group: selected_group.replace("_", " "), gpa_column: "Average GPA"},
                color_discrete_sequence=["#7c3aed"],
                template="plotly_white",
            )
            fig_grouped.update_yaxes(range=[0, 4])
            st.plotly_chart(fig_grouped, width="stretch")
        else:
            st.info("A numeric GPA column and categorical columns are required.")

st.caption("Python · Pandas · Plotly · Streamlit · Docker")