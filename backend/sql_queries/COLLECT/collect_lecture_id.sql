-- Could be useful as an initial function, 
-- then just need to use the ID for future queries 
-- on a lecture.

SELECT id FROM lectures
WHERE created_at LIKE 'yyyy-mm-dd%' AND module_code = 'CS1106';