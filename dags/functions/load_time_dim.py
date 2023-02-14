def load_time(**kwargs):
    # import libraries
    from datetime import datetime, timedelta, date
    import pandas as pd
    
    # get yesterday date in the format yyyy-mm-dd
    yesterday = date.today() - timedelta(days = 1)

    # getting the connection to the database
    connection = kwargs['connection']

    # getting existing dates
    existing = pd.read_sql("SELECT time_id ,time_date FROM time_dim;", connection)
    # filling the table with yesterday dates if they don't exist in the db
    if (not yesterday in existing['time_date'].values):
        #  create an array with yesterday date and the corresponding hours
        dates = []
        for h in range(24):
            dates.append(
                {
                'date' : yesterday.strftime('%Y-%m-%d'),
                'day_of_week': yesterday.strftime('%A'),
                'time_day': yesterday.strftime('%d'),
                'time_month':yesterday.strftime('%m'),
                'time_year': yesterday.strftime('%Y'),
                'hour': h
                }
            )
        connection.execute("INSERT INTO time_dim (time_date, time_day_of_week, time_day, time_month, time_year, time_hour) VALUES (%(date)s, %(day_of_week)s, %(time_day)s, %(time_month)s, %(time_year)s, %(hour)s)", dates)