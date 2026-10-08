-- SQLite

-- SELECT * FROM lectures;

INSERT INTO lectures -- (id, lecture_title, module_code, created_at, slides_link)
VALUES (NULL, 'Programming 101', 'CS1106', '2026-10-08 11:00:00', NULL);

/* NULL as the id primary key works because of SQLite's Autoincrement. */

-- SELECT * FROM lectures;