# ETL-Airflow-Docker

This repo is dedicated to orchestrating an ETL job as a part of data engineering work. 
A simple extraction with web scraping a web page  followed by transforming the extracted data into useful and workable csv file and followed by loading the csv file created into a s3 bucket (amazon cloud account).

The outlook is as follows:

![Screenshot 2024-10-18 104120](https://github.com/user-attachments/assets/4d8c13d8-2a88-40bd-86aa-0efa6af13097)



# Requirements
1. Docker-Desktop.
2. Python.
3. Code editor (VS code preferrable).

# Steps to follow:
1. ## Creating directory.
   Create a directory for the project on system.
   The structure follows as:


   ![Screenshot 2024-10-18 110157](https://github.com/user-attachments/assets/445ac86b-ba1b-437b-a4c5-fb78dd55928c)



2. ## docker-compose.yaml file creartion.
   In the airlow directory, create a yaml file, it can be copied from the repo 
   or can be download from the official website for that follow
   1. `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'`     to run on command to install directly.
   2. `https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml`   follow the link.
   and save it as file in the name of "docker-compose.yaml".

   ## Changes to .yaml file.
   Refer to the docker-compose.yaml file in the repo for clearity.
   1. Bydefault it uses **CeleryExecutor** for execution and we are fine with **LocalExecutor**, so goahead and make the changes.
   2. Remove the auxilary components that **CeleryExecutor** needs as we dont use it.
   3. We wont be using **Rediss** for this project so remove it to.
   4. Atlast you will find a **flower** section in the file, we dont need that as well.

3. ## Required floder.
   We need to create a couple of folders in the airflow folder in the name of,
   1. plugins
   2. logs
   3. dags
   4. config

   After creating them the structure sholud look like this:
   
   ![Screenshot 2024-10-18 111922](https://github.com/user-attachments/assets/696fa361-8af8-40dd-8775-de5750195d5c)


4. ## Starting docker for airflow.
   In the command line execute `Docker-compose up`, it will start pulling the requirements and installing them.
   In the mean while make sure the docker desktop is running in the background.
   It may take a while for them to get installed. When the installation has completed, you can see a new container created in the docker with name **airflow**.
   In the container section we can see like this:

  ![Screenshot 2024-10-18 112839](https://github.com/user-attachments/assets/7f853717-e49e-4a4d-b3ff-ee2a9ab7c549)


5. ## Airflow Web UI.
   In the web browser, open this ***http://127.0.0.1:8080/home***
   It will open up the web page for airflow UI in the port no. 8080  as specified in the .yaml file.
   At the login page use <br>
   username: ***airflow*** <br>
   password: ***airflow*** <br>
   to login in. Airflow home page will be open up.

6. ## Creating our dag.
   In the dags folder we will be creating a python file ***webscraping-ETL.py*** for the dags to be reflected in airflow.
   The python file contain simple function that reflects the extraction and transfoamtion and loading aspects.

   The structure sholud look like this:
   
  ![Screenshot 2024-10-18 114952](https://github.com/user-attachments/assets/02637358-1ee1-4150-9fed-83d97054f1db)


   Extraction. <br>
   
 `BeautifulSoup` which is avaliable in the `bs4` python liberary.
   
  Transformation. <br>
    
  python's `pandas` library is needed.  <br>
   
   Load. <br>
    
   For this project, s3 bucket from aws account is choosen to load the data transformed.
   For this first we need to create a s3 bucket in the aws account. <br>
   create a IAM role and give the access to s3 bucket for that role and copi the ***Access key id*** and ***Access key password***  these will be needed to createa connection in the airflow UI. <br>
   We will be using `S3Hook` liberary to connect AWS s3 with airflow.
   In the airflow UI, in the Admin section navigate to and create a new connection with following, <br>
   connection Id: `aws_s3_conn` <br>
   connection type: `Amazon web server` <br>
   AWS Access key ID: `Your_Access_key` <br>
   AWS Access key Password: `Your_Access_key_Passowrd` <br>
   With that the connection is set.
   
8. To run the dag open the dag >> unpause the dag  >> run dag using the run buttun at top left.
   If you switch to the graph section you can see the each task of dags and their status.


![Screenshot 2024-10-18 120947](https://github.com/user-attachments/assets/0d95bfce-3e05-453c-b4c2-b0588523f2ee)


   

   You can verify the sucessful completion of the dag run if you see all green at the status bar.
   You can also verify the s3 bucket to reflect the file being uploaded.
     
   
   
