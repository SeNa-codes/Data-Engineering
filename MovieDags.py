from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from datetime import datetime, timedelta
import requests
import json
import pandas as pd


MOVIE_API_URL = "http://www.omdbapi.com/?i=tt3896198&apikey=b1715467"
API_KEY = "b1715467"  
S3_BUCKET = "your-s3-bucket"   
S3_KEY = "movie_data/movies.json"  

# Fetch Movie Data
def FetchData():
    
    response = requests.get(MOVIE_API_URL, params={"api_key": API_KEY})
    data = response.json()
    movies = data.get("results", [])
    
    FilePath = "/tmp/movies.json"
    with open(FilePath, "w") as file:
        json.dump(movies, file)
    
    return FilePath

# Transform Movie Data 
def TransformData():
    """
    Read the JSON file, convert the data to a DataFrame,
    select specific columns, and save as a CSV file.
    """
    InputPath = "/tmp/movies.json"
    with open(InputPath, "r") as file:
        movies = json.load(file)
    
    # Create a DataFrame and select only the necessary columns
    df = pd.DataFrame(movies)
    columns_to_keep = ["id", "title", "release_date", "vote_average", "popularity"]
    df = df[columns_to_keep]
    
    OutputPath = "/tmp/movies_transformed.csv"
    df.to_csv(OutputPath, index=False)
    
    return OutputPath

# Default DAG Arguments 
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='movie_etl',
    default_args=default_args,
    description='ETL pipeline for data',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Fetch movie data from the API
    fetch_task = PythonOperator(
        task_id='fetch_data',
        python_callable=FetchData
    )

    # Transform the fetched data into a CSV file
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=TransformData
    )

    # Upload the transformed CSV file to S3
    upload_s3_task = LocalFilesystemToS3Operator(
        task_id='upload_to_s3',
        filename='/tmp/movies_transformed.csv',
        dest_bucket=S3_BUCKET,
        dest_key=S3_KEY,
        aws_conn_id='aws_default',
        replace=True,
    )

    # Order of tasks
    fetch_task >> transform_task >> upload_s3_task
