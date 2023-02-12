CREATE TABLE IF NOT EXISTS location_dim (
    location_id INT PRIMARY KEY auto_increment,
    latitude VARCHAR(100),
    longitude VARCHAR(100)
);