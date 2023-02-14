# Crime-Analysis-SFDP
Getting Data from the SFDP dataset, integrating this data into a Datamart, and then proceed with the analysis through a dashboard.

## Objective
The objective is to perform analysis on incidents happening in San Francicso via indicators in a dashboard while going through the integration phase after performing some transformations. This project is done in order to be familiar with some data engineering and data analysis tools : Apache Airflow, Docker, Python and Power BI.

## Steps
* Some explanations and remarks about the dataset. 
* Designing the Datamart model. 
* Explaining the DAG.
* Fetching the relevant data i.e the incidents that have been reported the day before.
* Create the tables if they have not been yet created.
* Loading the dimension tables with the appropriate data.
* Loading the fact table.
* Creating the dashboard after connecting Power BI with our Datamart.

## Some explanations and remarks about the dataset
The [dataset](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/data "SFDP dataset") used in this project contains information about the incidents that was reported in San Francisco Polcie Department, it contains multiple columns, the columns that will be used for the project :

* **incident_id :**  a system generated identifier for the incident report. 
* **incident_description :** the description of the incident.
* **incident_datetime :** The date and time when the incident occurred.
* **incident_day_of_week**
* **incident_category**
* **incident_subcategory**
* **report_datetime :** the date and time when the report was filed.
* **report_type_code :** a system code for report types.
* **report_type_description**
* **police_district :** the police district where the incident occured.
* **latitude :** the latitude coordinate in WGS84.
* **longitude**
* **resolution :** The resolution of the incident at the time of the report. It can be either of (*Cite or Arrest Adult*, *Exceptional Adult*, *Open or Active*, *Unfounded*).

**It is worth mentioning that the *incident_id* can be repeated in multiple rows in the dataset, that is due to the fact the incident can belong to multiple categories.** 


<picture>
<img alt="incident_id repetition" src="https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/incident_id%20repetition.png">
</picture>


In the example above, 1242744 is repeated three times for the categories *Assault*, *Robbery* and *Weapons Carrying Etc*.




## Designing the Datamart model
![alt text](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/incidents_dimensional_modeling.drawio.png "Datamart model")

The model contains 4 dimensions and one fact table. Besides, a table *incident_category_ is used to normalize *incident* and *category*. However, it is also possible to add the category in the fact table in a denormalized manner so that the *incident_id* is repeated in the table, this solution can be used when we want to avoid an additional join operation; in contrast, the table will be harder to maintain in comparison to the previous approach.


## Explaining the DAG
![image](https://user-images.githubusercontent.com/48518599/218859031-971ac83c-e1a2-44fe-9f46-e88ab5aa62b4.png "DAG")

The **Directed Acyclic Graph** in **Apache Airflow** represents a series of tasks.\\
First, the data is retrieved from the API. Then, the dimension tables are loaded after opening a conenction to the database. After that, the fact table and the *incident_cateogory* table are loaded. Finally, the connection to the database is closed.

## Fetching the relevant data

In this step, the data is fetched from the API provided by the SFPD that contains information about the incidents from 2018 to present that is updated every day.\\
the goal is to retrieve only yesterday's data, However if we used the API endpoint provided https://data.sfgov.org/resource/wg3w-h783.csv, it will load 5000 random rows from the dataset. Fortunately, the API provides different ways to query the dataset using filters and [SoQL Queries](https://dev.socrata.com/docs/queries/ "click for more details on it"). Therefore, it is possible to get only yesterday's data.\\
the task code is in [get data from api file](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/dags/functions/get_data_from_api.py)






