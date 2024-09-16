CREATE TABLE team
(
    id        INTEGER NOT NULL,
    team_name VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE team_set
(
    id       INTEGER NOT NULL,
    team_id  INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    fte      FLOAT   NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT id_team_id FOREIGN KEY (team_id) REFERENCES team (id),
    CONSTRAINT id_staff_id FOREIGN KEY (staff_id) REFERENCES staff (id)
);

CREATE TABLE staff
(
    id             INTEGER NOT NULL,
    staff_name     VARCHAR NOT NULL,
    staff_date     DATE    NOT NULL,
    staff_datetime DATETIME,
    staff_active   BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);
