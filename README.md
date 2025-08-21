BayirExpress Data Pipeline & Dashboard

🚀 BayirExpress is a crowd-shipping and exchange platform I have built.
This repository hosts the data pipeline (ETL workflows) and dashboard for monitoring users, announcements, and platform activity.

📌 Project Overview

The repo contains two main components:

Data Pipeline (ETL with Airflow & Python)

Extracts raw data from MongoDB (users, announcements, visitors).

Cleans and validates the data (Pydantic + Pandas).

Loads the transformed data into CSV/Parquet files for analysis.

Orchestrated with Apache Airflow and containerized with Docker.

Dashboard (Streamlit + Plotly)

Visualizes platform metrics (users, ads, traffic).

Interactive charts for monitoring growth and usage.

Supports filtering by dates, ad type, and user activity.


📊 Features

Pipeline

Automated ETL with Airflow DAGs.

Modular extract/transform/load functions.

Data quality checks with Pydantic.

Dashboard

Metrics on active users, ads, and traffic.

Interactive Plotly visualizations.



MIT License © 2025 BayirExpress
