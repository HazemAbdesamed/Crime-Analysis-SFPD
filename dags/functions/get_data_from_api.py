def getData(**kwargs):
   import pandas as pd
   from datetime import date
   from datetime import timedelta


   # getting the connection to the database
   connection = kwargs['connection']

   yesterday = pd.Timestamp(date.today() - timedelta(days = 1))
   
   # formatting the url
   url = "https://data.sfgov.org/resource/wg3w-h783.csv?$where=report_datetime between '{0}' and '{1}' &$order=report_datetime DESC".format(yesterday.date(), yesterday.date() + timedelta(days=1))
   url = url.replace(" ","%20")
   url = url.replace("'","%27")
   df = pd.read_csv(url)

   # selecting the columns
   df = df[['incident_id', 'incident_description', 'incident_datetime', 'incident_day_of_week', 'incident_category', 'incident_subcategory', 'report_datetime', 'report_type_code','report_type_description', 'police_district', 'latitude', 'longitude', 'resolution']]
   
   # some transformations
   df['incident_datetime'] = pd.to_datetime(df['incident_datetime'])
   df['report_datetime'] = pd.to_datetime(df['report_datetime'])
   df['incident_category'] = df['incident_category'].apply(str)
   df['incident_subcategory'] = df['incident_subcategory'].apply(str)
   df['incident_description'] = df['incident_description'].apply(lambda d: d.replace(',', '-') )
   df['incident_category'] = df['incident_category'].apply(lambda d: d.replace(',', '-') )
   df['incident_subcategory'] = df['incident_subcategory'].apply(lambda d: d.replace(',', '-') )
   df['incident_category'].fillna('', inplace=True)
   df['incident_subcategory'].fillna('', inplace=True)
   df.drop_duplicates(inplace=True)
   df.loc[df['incident_category']=='nan', ['incident_subcategory', 'incident_category']] = ''
   
   # adding data to a staging table
   if(len(df)>0):
      df.to_sql('crimes', connection, if_exists='replace', index=False )
   # df.to_csv("/usr/local/airflow/csv_files_airflow/crimesStaging.csv", index=False)

   