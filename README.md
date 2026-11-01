# 🚆 End-to-End Commuter Life Satisfaction ETL Pipeline

A lightweight, containerized data pipeline that extracts, cleans, transforms, and loads urban commuter life satisfaction survey data into an isolated **PostgreSQL** database using **Docker** and **Docker Compose**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Desktop-2496ED?logo=docker)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas)

---

## 📌 1. Business Understanding

### Background
In major metropolitan regions (such as the Greater Jakarta / Jabodetabek area), millions of workers spend 1 to 4 hours every day commuting. Daily transit factors—including transit mode, travel duration, and congestion—directly correlate with stress levels, productivity, and overall psychological well-being (*Subjective Well-Being*).

### Problem Statement
Raw survey datasets frequently contain cryptic numerical questionnaire codes (`a1`, `a2`, `b1`), missing values, and unstandardized schemas. Without automated data preparation, this raw data is inaccessible for business analysts, urban planners, and decision-makers.

### Project Objectives
- Automate a clean and reproducible **Extract, Transform, Load (ETL)** pipeline without heavyweight orchestration overhead.
- Perform *semantic data transformation* (mapping encoded survey values into descriptive, human-readable labels).
- Deliver an analytics-ready *Single Source of Truth* in a relational PostgreSQL database containerized with Docker.

---

## 🏗️ 2. Pipeline Architecture

```text
[ data_commuter.csv ] (Raw Kaggle Dataset)
         │
         ▼ (Extract)
    [ Pandas DataFrame ]
         │
         ▼ (Transform)
    ├── Standardize column names to snake_case
    ├── Semantic Renaming (a1 -> gender_code, a2 -> age, b1 -> transport_code)
    ├── Value Mapping (1 -> 'Male', 4 -> 'KRL Commuter Line', etc.)
    └── Age Binning (<25, 25-40, 41-60, >60 years old)
         │
         ▼ (Load via SQLAlchemy)
[ PostgreSQL Database (Docker Container) ]
```

---

## 📊 3. Key Insights from the Data

Based on analysis of 384 commuter survey respondents:
- **Public Transit Dominance**: Approximately **61.7% of commuters (237 respondents)** rely primarily on the **KRL Commuter Line**, confirming it as the backbone of daily urban transit.
- **Demographics**: Composed of **74.2% Male** (285 respondents) and **25.8% Female** (99 respondents).
- **Core Age Group**: The majority of commuters fall within the core productive demographic of **25–40 years old**.

---

## 📁 4. Project Structure

```text
commuter-etl/
├── data/
│   └── data_commuter.csv      # Raw survey dataset
├── src/
│   └── etl.py                 # Core ETL pipeline script (Extract, Transform, Load)
├── Dockerfile                 # Docker build specification for Python ETL environment
├── docker-compose.yml         # Container orchestration for PostgreSQL & ETL runner
├── requirements.txt           # Python library dependencies
├── .gitignore                 # Git ignore rules for clean repository state
└── README.md                  # Project documentation
```

---

## 🚀 5. Getting Started

### Prerequisites:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### How to Run:
1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/commuter-etl.git
   cd commuter-etl
   ```

2. **Build and run the pipeline and database with a single command:**
   ```bash
   docker compose up --build
   ```

3. **Verify the transformed data in PostgreSQL:**
   ```bash
   docker exec -it postgres_commuter psql -U postgres -d commuter_db -c "SELECT usia, kelompok_usia, jenis_kelamin, nama_transportasi FROM dim_kepuasan_komuter LIMIT 5;"
   ```

4. **Tear down the containers:**
   ```bash
   docker compose down
   ```

---

## 📤 6. Publishing to GitHub

To push this project to your personal GitHub account:

1. Create a new repository on [GitHub](https://github.com/new) named `commuter-etl` (leave *Add README* unchecked).
2. Execute the following commands in your terminal:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commuter etl pipeline with docker and postgres"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/commuter-etl.git
   git push -u origin main
   ```