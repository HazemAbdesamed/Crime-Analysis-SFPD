def get_hour_str(h):
    if h >= 10 :
        return str(h)
    else :
        return "0"+str(h)    

def load_fact(**kwargs):
    # import libraries
    import pandas as pd
    from datetime import datetime as dt, date    

    # getting the connection to the database
    connection = kwargs['connection']

    # get the data from the source
    source = pd.read_sql_query("SELECT * FROM crimes;", connection)

    # get data from dimensions
    time_dim = pd.read_sql_query("SELECT * FROM time_dim;", connection)
    loc_dim = pd.read_sql_query("SELECT * FROM location_dim;", connection)
    report_dim = pd.read_sql_query("SELECT * FROM report_dim;", connection)
    existing_fact = pd.read_sql_query("SELECT * FROM incident_fact;", connection)

    # transform  

    #time
    source["incident_time_join"] = source["incident_datetime"].dt.strftime("%Y %m %d %H")
    source["report_time_join"] = source["report_datetime"].dt.strftime("%Y %m %d %H")
    time_dim['time_hour']= time_dim['time_hour'].apply(get_hour_str)
    time_dim['time_date']= time_dim['time_date'].apply(str).apply(lambda d : d.replace("-", " "))
    time_dim["time_join"] = time_dim["time_date"] + " " + time_dim["time_hour"]
    
    #location
    source['latitude'].fillna('', inplace=True)
    source['longitude'].fillna('', inplace=True)
    source["loc_indicator"] = source['latitude'].astype(str) + "a" + source['longitude'].astype(str)
    loc_dim.drop_duplicates(subset=['latitude', 'longitude'], inplace= True)
    loc_dim["loc_indicator"] = loc_dim['latitude'].str.cat(loc_dim['longitude'], sep='a')
    #report
    source["rep_indicator"] = source['report_type_code'].str.cat(source['report_type_description'], sep='$')
    report_dim["rep_indicator"] = report_dim['report_code'].str.cat(report_dim['report_description'], sep='$')

    # perform the joins 
   
    #report
    joined = pd.merge(source, report_dim, on ="rep_indicator", how="left")
    joined['report_id'].fillna(0, inplace=True)
    #location
    joined = pd.merge(joined, loc_dim, on ="loc_indicator", how="left")
    joined['location_id'].fillna(0, inplace=True)
    #time
    joined = pd.merge(joined, time_dim, left_on= 'incident_time_join', right_on='time_join', how='left') 
    joined_with_report_time = pd.merge(joined, time_dim, left_on= 'report_time_join', right_on='time_join', how="left")
    joined_with_report_time['time_id_x'].fillna(0, inplace=True)
    joined_with_report_time['time_id_y'].fillna(0, inplace=True)
    #rename columns
    joined = joined_with_report_time.rename(columns={'time_id_x' : 'incident_time_id', 'time_id_y' : 'report_time_id', 'location_id':'incident_location_id', 'cat_id':'incident_category_id'})
    
    # append to the fact table the new data
    fact = joined[['incident_id', 'report_id', 'incident_time_id', 'report_time_id', 'incident_location_id', 'police_district', 'incident_description', 'resolution']].reset_index()
    
    # execute the query
    connection.execute("INSERT INTO incident_fact (incident_id, report_id, incident_time_id, report_time_id, incident_location_id, police_district, incident_description, resolution) VALUES (%(incident_id)s, %(report_id)s, %(incident_time_id)s, %(report_time_id)s, %(incident_location_id)s, %(police_district)s, %(incident_description)s, %(resolution)s) ON DUPLICATE KEY UPDATE resolution = VALUES(resolution)", fact.to_dict('records'))