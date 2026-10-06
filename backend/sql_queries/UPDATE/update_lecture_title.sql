UPDATE lectures
SET lecture_title = 'Test Title 2'
WHERE module_code = 'CS1106' AND created_at LIKE 'yyyy-mm-dd%';

-- SELECT * FROM lectures;