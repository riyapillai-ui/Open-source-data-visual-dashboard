# Student Performance Analysis Dashboard

An open-source Streamlit dashboard for exploring how study habits, attendance,
parental involvement, and extracurricular activities relate to student
academic performance.

## Problem statement

How do study habits, attendance, parental involvement, and extracurricular
activities relate to students' academic performance?

## Stack

- Python 3.11
- Streamlit
- Pandas
- Plotly
- Docker

## Run on Replit

The project is configured with a Replit workflow. Start the application and
open the preview, or run it locally with:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=5000
```

## Local setup

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard reads `data/student_performance.csv`. It now uses the supplied
Students Performance Dataset with 2,392 student records. Preprocessing removes
duplicate and fully empty rows, fills missing numeric values with medians, and
decodes the dataset's numeric category codes into readable labels. The source
dataset provides `Absences` rather than `Attendance`, so the second analysis
view correctly presents Absences vs GPA.

## Docker setup

```bash
docker compose up --build
```

Then open <http://localhost:8501>.

## Dashboard features

1. Multi-select filters for categorical student characteristics
2. Grade-distribution donut chart
3. Average GPA by weekly study-time line chart
4. Average GPA by absence-band line chart
5. Average GPA by a selected student characteristic bar chart
6. Student, GPA, absences, and study-time summary metrics

## CA3 progress

### Phase 1 — Data ingestion

- [x] Load the local CSV using Pandas
- [x] Remove duplicate records
- [x] Remove completely empty rows
- [x] Fill missing numeric values with column medians

### Phase 2 — Visualisation

- [x] Create the Streamlit interface
- [x] Add interactive filters
- [x] Add three Plotly visualisations
- [x] Add dashboard metrics

### Phase 3 — Deployment

- [x] Create Dockerfile
- [x] Create docker-compose.yml
- [x] Configure a Replit workflow
- [ ] Push the final version to GitHub
- [ ] Demonstrate the containerised dashboard

## Assessor Q&A

**Why Streamlit?** Streamlit creates an interactive Python dashboard without
requiring a separate frontend, and works naturally with Pandas and Plotly.

**Why Docker?** Docker makes the Python version and dependencies reproducible
on another computer.

**Why a local CSV?** This is a small, static educational dataset, so a local
CSV keeps the CA3 project focused and avoids unnecessary database
infrastructure.

**Why main and dev branches?** Development can be tested on `dev` while
`main` remains the stable submission version.

**Why three visualisations?** Three focused views answer the problem statement
while keeping the dashboard understandable and achievable within scope.

## License

This project uses open-source software and a publicly available dataset.
Check the original dataset source for its data license before redistribution.