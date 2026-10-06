-- SELECT * FROM lectures;

DELETE FROM lectures
WHERE created_at LIKE '2026-10-08%' AND module_code = 'CS1111';

-- SELECT * FROM lectures;