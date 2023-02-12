CREATE TABLE IF NOT EXISTS time_dim (
    time_id INT PRIMARY KEY auto_increment,
    time_date date,
    time_hour int,
    time_day_of_week VARCHAR(10),
    time_day int,
    time_month int,
    time_year int
);