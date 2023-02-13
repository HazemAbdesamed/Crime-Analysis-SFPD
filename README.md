# Crime-Analysis-SFDP
Getting Data from the SFDP dataset, integrating this data into a Datamart, and then proceed with the analysis through a dashboard.

## Objective
The objective is to perform analysis on incidents happening in San Francicso via indicators in a dashboard while going through the integration phase after performing some transformations. This project is done in order to be familiar with some data engineering and data analysis tools : Apache Airflow, Docker, Python and Power BI.

## Steps
* Some explanations and remarks about the dataset 
* Designing the Datamart model. 
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
* **resolution :** The resolution of the incident at the time of the report. It can be either (*Cite or Arrest Adult*, *Exceptional Adult*, *Open or Active*, *Unfounded*).

**It is worth mentioning that the *incident_id* can be repeated in multiple rows in the dataset, that is due to the fact the incident can belong to multiple categories.** 


<picture>
<img alt="incident_id repetition" src="https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/incident_id%20repetition.png">
</picture>


In the example above, 1242744 is repeated three times for the categories *Assault*, *Robbery*, *Weapons Carrying Etc*.




## Designing the Datamart model
![alt text](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/incidents_dimensional_modeling.drawio.png "Datamart model")

The model contains 4 dimensions and one fact table, in addition a table used to normalize incident and categories. It is also possible to add the category in the fact table in a denormalized manner so that the *incident_id* is repeated in the table, this solution can be used when we want to avoid an additional join operation, but the table will be harder to maintain in comparison to the previous approach.






