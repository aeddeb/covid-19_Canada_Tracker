# COVID-19 Canada Tracker

A data pipeline constructed with dbt, Docker, Airflow, Terraform, and GCP.

## Overview
### Purpose
The purpose of this project is to provide a dashboard to allow users to track COVID-19 related data in Canada. The related data includes, but is not limited to, COVID-19 cases, vaccinations, deaths, and recoveries.

### Process
The data ingested through a batch job on a daily basis orchestrated through Airflow. Once ingested into a data lake (GCS), it is loaded into Bigquery where it is transformed via dbt into a clean timeseries table which is then used to create the dashboard. 

### Dataset
- Data source: Canada COVID-19 Data (https://api.opencovid.ca/)

For more information on the dataset, please refer to their git repo: https://github.com/ccodwg/Covid19Canada.

## Technical Description

### Tools and Technologies
- Cloud - Google Cloud Platform
- IaaC - Terraform
- Containerization - Docker
- Orchestration - Airflow
- Transformation - dbt
- Data Lake - Google Cloud Storage
- Data Warehouse - BigQuery
- Data Visualization - Data Studio

### Architecture
![COVID-19 Canada Project Architecture](images/COVID-19_Canada_Project_Architecture.png)

## Dashboard
![COVID-19 Canada Tracker](images/Covid-19_Canada_Tracker-1.png)


## Improvements
- Create dev and prod environments
- Add tests
- Add CI/CD pipeline

### Credit
A big thank you goes to the team at [Data Talks Club](https://datatalks.club/) for organizing a free online Data Engineering bootcamp!

If interested, you can go through the bootcamp at your own pace. The bootcamp is linked here:
- github repo: https://github.com/DataTalksClub/data-engineering-zoomcamp
- youtube series: https://www.youtube.com/watch?v=bkJZDmreIpA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb 

This submission was my final project for the bootcamp.


## Brief Instructions to Reproduce this Project
*(More in-depth instructions to be provided)*
1. Create a google cloud platform account on GCP.
2. Create VM on Google Cloud and install Ubuntu 20.04
3. Create google service account with the appropriate permissions.
4. In your VM, install python, docker, terraform and git.
5. In your VM, clone the codes from this git repository and change the variables to the new environment. 
    * terraform: main.tf, variables.tf
    * airflow: Dockerfile, docker-compose.yaml
6. Run terraform to build the services in GCP.
7. Run docker compose in the airflow folder to start up the dags.
