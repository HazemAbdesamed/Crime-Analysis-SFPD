# Crime-Analysis-SFDP
Getting Data from the SFDP dataset, integrating this data into a Datamart, and then proceed with the analysis through a dashboard.

## Objective
The objective is to perform analysis on incidents happening in San Francicso via indicators in a dashboard while going through the integration phase after performing some transformations. This project is done in order to practice and be familiar with some data engineering and data analysis tools : **Apache Airflow**, **Docker**, **Python** and **Power BI**.

## Steps
* Some explanations and remarks about the dataset. 
* Designing the Datamart model. 
* Explaining the DAG.
* Fetching the relevant data i.e the incidents that have been reported the day before.
* Create the tables if they have not been yet created.
* Loading the dimension tables with the appropriate data.
* Loading the fact table and the *incident_category* table.
* Creating the dashboard after connecting Power BI to the Datamart.
* Final thoughts.

## Some explanations and remarks about the dataset
The [dataset](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/data "link to SFPD dataset") used in this project contains information about the incidents that was reported in San Francisco Polcie Department, it contains multiple columns, the columns that will be used for the project :

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
<img alt="incident_id repetition" src="https://user-images.githubusercontent.com/48518599/218886739-8c63bdf9-4314-4eba-884b-2a2bec3b8bde.png">
</picture>


In the example above, 1242744 is repeated three times for the categories *Assault*, *Robbery* and *Weapons Carrying Etc*.




## Designing the Datamart model
![alt text](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/incidents_dimensional_modeling.png "Datamart model")

The model contains 4 dimensions and one fact table. Besides, a table *incident_category* is used to normalize *incident* and *category*. However, it is also possible to add the category in the fact table in a denormalized manner so that the *incident_id* is repeated in the table, this solution can be used when we want to avoid an additional join operation; in contrast, the table will be harder to maintain in comparison to the previous approach.

The time dimension is a role playing dimension which will serve in keeping track of incidents and reports dates. 

The grain would be that each row int the fact table gives inforamtion about the incident that took place in a location at a time and reported at a time belonging to a category filed by a police district with a resolution status.


## Explaining the DAG
![image](https://user-images.githubusercontent.com/48518599/218859031-971ac83c-e1a2-44fe-9f46-e88ab5aa62b4.png "DAG")

The **Directed Acyclic Graph** in **Apache Airflow** represents a series of tasks.

First, the data is retrieved from the API and is stored in a staging table. Then, the dimension tables are loaded after opening a connection to the database. After that, the fact table and the *incident_cateogory* tables are loaded. Finally, the connection to the database is closed.

## Fetching the relevant data

In this step, the data is fetched from the API provided by the SFPD that contains information about the incidents from 2018 to present, the dataset is updated every day.

The goal is to retrieve only yesterday's data; However, if we used the API endpoint provided https://data.sfgov.org/resource/wg3w-h783.csv, it will load 5000 random rows from the dataset. Fortunately, the API provides different ways to query the dataset using filters and [SoQL Queries](https://dev.socrata.com/docs/queries/ "click for more details on it"). Therefore, it is possible to get only yesterday's data. We then insert this data to a staging table *crimes*.

The task code can be found in [get data from api file](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/blob/main/dags/functions/get_data_from_api.py).

## Create the tables if they have not been yet created.

The script for the creation of the staging, dimension and fact tables can be found in [db_data folder](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/tree/main/db_data).

## Loading the dimension tables with the appropriate data.

The dimension tables loading step is where the dimension tables are loaded from the data that is present in the staging table in a correct manner.

Only yesterday's date is loaded into the time dimension table.

The logic followed for the other dimensions : 
<pre><code>
- Distinct values related to the dimension are extracted from the staging table and are loaded in a python dataframe <b>df1</b> and perform some transformations.
- Extract data that is present in the dimension table and put it in <b>df2</b> and perform some transformations.
- Retrieve only the values that are in the <b>df1</b> and not in <b>df2</b> and put them in <b>df3</b>.
- App <b>df3</b> to the dimension table.
</pre></code>
The tasks codes are present in the [functions folder](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/tree/main/dags/functions).

## Loading the fact table and the incident_category table
After loading the dimension tables of the datamart, the fact table is loaded by applying joins between the dimension tables and the staging table.

The logic followed is :
<pre><code>
- Extract data from the staging table <b>ST</b> and performing some transformations.
- Extract the dimension tables <b>DTs</b> and performing some transformations.
- Perform joins between <b>ST</b> and <b>DTs</b>.
- Append new data to the fact table.
</pre></code>
This task code can be found in the [load fact file](https://github.com/HazemAbdesamed/Crime-Analysis-SFDP/tree/main/dags/functions/load_fact.py).

The logic followed for loading *incident_category* table is :
<pre><code>
- Extract distinct value pairs of <i>incident_id</i> <i>and category_id</i> and put them in <b>df1</b>.
- Extract data that is present in the existing <i>incident_category</i> table and the it in <b>df2</b>.
- Retrieve data that is present in <b>df1</b> and not present in <b>df2</b> and put it in <b>df3</b>.
- Append <b>df3</b> to the <i>incident_category</i> in the datamart.
</pre></code>

## Creating the dashboard after connecting Power BI to the Datamart.
![alt text](https://user-images.githubusercontent.com/48518599/218880103-90f62a5a-90f4-431f-a89d-b71bfb1f059e.png)

The dashboard contains information about the number of incidents by date and time, it is possible to navigate through the hierarchy and to filter by any year, month date or day of week. It also contains information about the number of incidents rate grouped by category and subcategory, the number of incidents by the resolution status in a pie chart and in the map.

## Final thoughts
One thing that i wanted to improve, is the resolution status of the incident. After reading the API docs, I'm still not sure exactly of what happens to the dataset when an incident gets resolved. After loading all the dataset and querying it to find if any incident has changed is resoltion, the result was an empty set.

![alt text](https://user-images.githubusercontent.com/48518599/218883787-631531e7-3db9-4b14-b6dc-32005c3af849.png "no incident has changed its resolution in the dataset")

Besides, the approach followed when normalizing *incidents* and *category* data helps in updating only one row for each incidents in the fact table. In addition, adding the information of the date and time of the resolution to the dataset would be a good plus. This way, we can apply SCD concept in the fact table and we can get the time taken to resolve each incident.

**Any advice, remark or criticism is welcomed**.









