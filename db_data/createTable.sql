CREATE TABLE IF NOT EXISTS crimes (
    incident_id INT PRIMARY KEY,
    incident_datetime DATETIME,
    incident_day_of_week VARCHAR(10),
    incident_category VARCHAR(100),
    incident_subcategory VARCHAR(100),
    report_datetime DATETIME,
    report_type_code VARCHAR(10),
    report_type_description VARCHAR(255),
    police_district VARCHAR(100),
    latitude VARCHAR(100),
    longitude VARCHAR(100),
    resolution VARCHAR(50)
);