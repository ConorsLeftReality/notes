-- SELECT module_id,module_messages FROM modules
-- WHERE module_id = 'CS1107';

UPDATE modules
SET module_message = 'message_here'
WHERE module_id = 'CS1107';

-- SELECT module_id,module_messages FROM modules
-- WHERE module_id = 'CS1107';