-- SQLite

/* module_id (TEXT), module_title (TEXT), enrolled (INTEGER NOT NULL CHECK (enrolled IN (0, 1))), year_of_study (INTEGER), semester (INTEGER), module_messages (TEXT) */

INSERT INTO modules -- (module_id, module_title, enrolled, year_of_study, semester, module_message)
VALUES ('CS1109','Intro to Relational Databases 3',1,1,1,'rm -rf /var/opt/gitlab/postgresql/data/ - some GitLab database enginner in January 2017');

-- SELECT * FROM modules;