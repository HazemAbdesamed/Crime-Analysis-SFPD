CREATE TABLE IF NOT EXISTS incident_category (
    incident_id INT,
    category_id INT,
    CONSTRAINT `inc_cat_pk` PRIMARY KEY(incident_id, category_id)
    -- CONSTRAINT `inc_fk` FOREIGN KEY(incident_id) REFERENCES incident_fact(incident_id),
    -- CONSTRAINT `cat_fk` FOREIGN KEY(category_id) REFERENCES category_dim(cat_id)
);
