# MLOps Lab 2: Multi-Model Pipeline with Apache Airflow

**Course**: IE7374 - MLOps, Northeastern University  
**Author**: Rahul Reddy Mandadi

## Overview

Airflow pipeline that trains and compares three ML models for ad click prediction, automatically selects the best one, and sends email notifications with results.

## Results

```
Logistic Regression: 97.00% (Winner)
Random Forest:       95.00%
Decision Tree:       93.00%
```

## Modifications from Original Lab 3

1. **Multi-model training**: Trains 3 algorithms instead of 1, auto-selects best
2. **Data validation**: Added summary task with dataset statistics
3. **Enhanced emails**: Includes all model scores and comparison
4. **Airflow 3.0 updates**: New import paths, fixed XCom serialization
5. **Docker deployment**: Uses official docker-compose setup

## Quick Start

```bash
# Create folders
mkdir -p ./logs ./plugins ./config
echo -e "AIRFLOW_UID=50000" > .env

# Initialize
docker compose up airflow-init

# Start Airflow
docker compose up

# Access UI: http://localhost:8080
# Login: airflow / airflow
```

## Run the Pipeline

1. Enable `ad_click_prediction_mlops` DAG
2. Click play button to trigger
3. Check `build_save_model_task` logs for results

## Structure

```
mlops-airflow-lab3/
├── docker-compose.yaml
├── dags/
│   ├── my_dag.py
│   ├── src/
│   │   ├── model_development.py
│   │   └── success_email.py
│   └── data/
│       └── advertising.csv
└── README.md
```

## Technologies

Apache Airflow 3.1.0, Docker, PostgreSQL, Redis, scikit-learn, pandas

## Original Source

Based on [Lab 3 from Professor Ramin Mohammadi's MLOps course](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Airflow_Labs/Lab_3)
