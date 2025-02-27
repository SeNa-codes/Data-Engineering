# Data-Engineering


Welcome to the **Introduction to Data Engineering** project! 

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Project Structure](#project-structure)

## Project Overview
This project covers:
- **Extracting** data from APIs (http://www.omdbapi.com/?i=tt3896198&apikey=b1715467)
- **Transforming** raw data into a structured format using ETL processes.
- **Loading** data into a database or data warehouse.
- **Automating** workflows using scheduling tools.

The goal is to build a simple ETL pipeline.

## Technologies Used
- **Python** for scripting and automation
- **Pandas** for data manipulation
- **Airflow** workflow orchestration
- **AWS* for virtual instance


### Setup Instructions
Install dependencies:
   ```sh
sudo apt install python3 python3-pip python3-dev python3-venv
python3 -m venv venv
pip install apache-airflow
pip install requests
pip install pandas
   ```

Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Configure environment variables (if needed) in `.env` file.
5. Run the pipeline script:
   ```sh
   python MovieDags.py
   ```

## Project Structure
```
├── data/                  # Data Extraction from Api
├── scripts/               # Data extraction and transformation scripts
├── MovieDags.py           # Entry point for the pipeline
├── requirements.txt       # Required dependencies
├── README.md              # Project documentation
```

