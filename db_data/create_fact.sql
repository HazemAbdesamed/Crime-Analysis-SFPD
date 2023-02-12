CREATE TABLE IF NOT EXISTS incident_fact (
    incident_id INT,
    report_id INT,
    incident_time_id INT,
    report_time_id INT,
    incident_location_id INT,
    incident_category_id INT,
    police_district VARCHAR(30),
    resolution VARCHAR(30),
    CONSTRAINT `incident_pk` PRIMARY KEY(incident_id),
    CONSTRAINT `report_fk` FOREIGN KEY(report_id) REFERENCES report_dim(report_id),
    CONSTRAINT `incident_time_fk` FOREIGN KEY(incident_time_id) REFERENCES time_dim(time_id),
    CONSTRAINT `report_time_fk` FOREIGN KEY(report_time_id) REFERENCES time_dim(time_id),
    CONSTRAINT `location_fk` FOREIGN KEY(incident_location_id) REFERENCES location_dim(location_id),
    CONSTRAINT `category_fk` FOREIGN KEY(incident_category_id) REFERENCES category_dim(cat_id)
);




