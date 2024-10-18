from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
import requests

from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.python import PythonOperator
# import s3fs
from airflow.providers.amazon.aws.hooks.s3 import S3Hook



url  = 'https://www.reneecosmetics.in/collections/all-products'


def extraction():
    
   
        page = requests.get(url)
        html_content = BeautifulSoup(page.text,'html.parser')
        div = html_content.find_all('div',class_ ='card')
        ratings = []
        count = []
        title = []
        regular_price = []
        final_price = []
        discount = []
        img_url = []
        for i in div:
            ratings.append(i.find(class_='jdgm-average_rating').text)

            count.append(i.find(class_ = 'jdgm-rating_count').text)

            title.append(i.find('span',class_ = 'text').text.strip())

            regular_price.append(i.find('dd',class_ = 'price__compare').text)

            final_price.append(i.find('span',class_ = 'price-item--sale').text)

            discount.append(i.find('span',class_ = 'label_sale').text[1:-5])

            img_url.append(i.find('img')['src'])
        data ={
            'title':title,
            'rating':ratings,
            'count':count,
            'regular price':regular_price,
            'final price':final_price,
            'discount':discount,
            'image Url':img_url}
        df = pd.DataFrame(data)
        return (df)


def upload_to_s3(df,bucket_name,file_name,aws_conn_id='aws_s3_conn'):                # aws_s3_conn  ---> connection id name created from admin section >> connection (in the airflow UI).
      csv_buffer = df.to_csv(index=False)
      s3_hook = S3Hook(aws_conn_id=aws_conn_id)
      s3_hook.load_string(
            string_data=csv_buffer,
            key=file_name,
            bucket_name=bucket_name,
             replace=True )
        
def upload_task(**kwargs):
      df = extraction()
      upload_to_s3(df,'AWS_s3_bucket_name_created','extracted_data.csv')   


default_args = {
     'owner': 'Your name',
     'start_date': days_ago(0),
     'email': ['your email'],
     'retries': 1,
     'retry_delay': timedelta(minutes=5),
}

dag = DAG(
     'WebScraping-etl-dag',
     default_args=default_args,
     description='My first DAG',
     schedule_interval=timedelta(days=1),
)



exec_extraction = PythonOperator(
    task_id = 'Extraction_taks',
    python_callable=extraction,
    dag=dag
)

exec_upload= PythonOperator(
      task_id='Upload_to_s3',
      python_callable=upload_task,
      dag=dag
)

exec_extraction >> exec_upload



