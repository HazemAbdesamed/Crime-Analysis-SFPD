def load_report(**kwargs):
    # import libraries
    import pandas as pd

    # getting the connection to the database
    connection = kwargs['connection']

    # get the existing data in the dimension table
    existing_data = pd.read_sql_query('SELECT report_code, report_description FROM report_dim;', connection)
    # get the data to be loaded from the source
    data = pd.read_sql_query("SELECT DISTINCT report_type_code, report_type_description FROM crimes ;", connection)
    data = data.rename(columns={'report_type_code' : 'report_code', 'report_type_description' : 'report_description'})  
    # concatenate the values of the latitude and longitude into a new column in both dataframes
    existing_data['indicator'] = existing_data['report_code'].str.cat(existing_data['report_description'], sep='$')
    data['indicator'] = data['report_code'].str.cat(data['report_description'], sep='$')
    # get the new data i.e data that is in the source and not in the dimension table    
    new_data = data[~data['indicator'].isin(existing_data['indicator'])].drop(columns=['indicator'])
    # removing empty rows
    new_data = new_data[~(new_data["report_code"] == "") | ~(new_data["report_description"] == "") ]
    new_data = new_data[~(new_data["report_code"] == "nan") | ~(new_data["report_description"] == "nan") ]
    # append new data to the dimension table
    new_data.to_sql('report_dim', connection, if_exists='append', index = False) 
