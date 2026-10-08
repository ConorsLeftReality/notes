-- INSERT INTO lectures (id,lecture_title, module_code, created_at, slides_link, week, filename)
-- VALUES (NULL, 'Programming 101', 'CS1106', '2026-10-08 11:00:00', NULL, '3', 'test.pdf');

SELECT filename FROM lectures
WHERE filename = 'test.pdf';