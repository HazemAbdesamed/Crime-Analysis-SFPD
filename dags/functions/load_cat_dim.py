def load_category(**kwargs):
    # import libraries
    import pandas as pd
    # from functions.db_connection import connection

    # getting the connection to the database
    connection = kwargs['connection']


    # get the existing data in the dimension table
    existing_data = pd.read_sql_query('SELECT subcategory, category FROM category_dim;', connection)
    print(existing_data)
    # get the data to be loaded from the source
    data = pd.read_sql_query("SELECT DISTINCT incident_subcategory, incident_category FROM crimes ;", connection)
    data = data.rename(columns={'incident_subcategory' : 'subcategory', 'incident_category' : 'category'})  
    # concatenate the values of the latitude and longitude into a new column in both dataframes
    existing_data['indicator'] = existing_data['subcategory'].str.cat(existing_data['category'], sep='$')
    data['indicator'] = data['subcategory'].str.cat(data['category'], sep='$')
    # get the new data i.e data that is in the source and not in the dimension table    
    new_data = data[~data['indicator'].isin(existing_data['indicator'])].drop(columns=['indicator'])
    # removing empty rows
    new_data = new_data[~(new_data["subcategory"] == "") | ~(new_data["category"] == "") ]
    new_data = new_data[~(new_data["subcategory"] == "nan") | ~(new_data["category"] == "nan") ]
    # append new data to the dimension table
    new_data.to_sql('category_dim', connection, if_exists='append', index = False) 