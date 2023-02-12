def load_inc_cat(**kwargs):
    # import libraries
    import pandas as pd

    # initialising the connection to the database
    connection = kwargs['connection']

    # get the existing data in the dimension table
    existing_data = pd.read_sql_query('SELECT incident_id, category_id FROM incident_category;', connection)
    # get the data to be loaded from the source
    data = pd.read_sql_query("SELECT  DISTINCT cr.incident_id as incident_id, cat.cat_id as category_id FROM crimes cr LEFT JOIN category_dim cat ON cat.subcategory = cr.incident_subcategory ", connection)

    # concatenate the values of the latitude and longitude into a new column in both dataframes
    existing_data['indicator'] = existing_data['incident_id'].astype(str) + "$" + existing_data['category_id'].astype(str)
    data['indicator'] =  data['incident_id'].astype(str) + "$" + data['category_id'].astype(str)
    # get the new data i.e data that is in the source and not in the dimension table    
    new_data = data[~data['indicator'].isin(existing_data['indicator'])].drop(columns=['indicator'])
    new_data.drop_duplicates(inplace=True)
    new_data.to_sql('incident_category', connection, if_exists='append' ,index=False)