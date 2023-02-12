def load_location(**kwargs):
    # import libraries
    import pandas as pd

    # initialising the connection to the database
    connection = kwargs['connection']

    # get the existing data in the dimension table
    existing_data = pd.read_sql_query('SELECT latitude, longitude FROM location_dim;', connection)
    # get the data to be loaded from the source
    data = pd.read_sql_query("SELECT latitude, longitude FROM crimes ;", connection)
    data['longitude'].fillna('', inplace=True)
    data['latitude'].fillna('', inplace=True)

    # concatenate the values of the latitude and longitude into a new column in both dataframes
    existing_data['indicator'] = existing_data['latitude'].str.cat(existing_data['longitude'], sep='a')
    data['indicator'] = data['latitude'].astype(str) + "a" + data['longitude'].astype(str)
    # get the new data i.e data that is in the source and not in the dimension table    
    new_data = data[~data['indicator'].isin(existing_data['indicator'])].drop(columns=['indicator'])
    # removing empty rows
    new_data = new_data[~(new_data["latitude"] == "") | ~(new_data["longitude"] == "") ]
    # removing duplicates
    new_data = new_data.drop_duplicates(subset=['latitude', 'longitude'])
    # append new data to the dimension table
    new_data.to_sql('location_dim', connection, if_exists='append', index = False)