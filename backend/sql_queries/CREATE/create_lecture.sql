-- SQLite

-- SELECT * FROM lectures;

/* id (INT), lecture_title (TEXT), module_code (TEXT), created_at (DATETIME), slides_link (TEXT) */
INSERT INTO lectures -- (id, lecture_title, module_code, created_at, slides_link)
VALUES (NULL, 'Programming 101', 'CS1106', '2026-10-08 11:00:00', NULL);

/* NULL as the id primary key works because of SQLite's Autoincrement. */

-- SELECT * FROM lectures;