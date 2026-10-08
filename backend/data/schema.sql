PRAGMA foreign_keys = ON;

CREATE TABLE modules (
  module_id       TEXT PRIMARY KEY NOT NULL,  -- The Module ID, one directory per module. Also used for directory name
  module_title    TEXT,                       -- Title of the module, used on frontend such as index pages
  enrolled        INTEGER NOT NULL CHECK (enrolled IN (0, 1)),  -- Whether we are enrolled, generation script stuff
  year_of_study   INTEGER NOT NULL,           -- Information for sorting files
  semester        INTEGER NOT NULL,           -- Which semester we study this module in. Also used for sorting
  module_messages TEXT                        -- Message displayed on the modules index page (usually a quote)
);

CREATE TABLE lectures (
  id            INTEGER PRIMARY KEY,          -- Randomly assigned id, no specific format
  lecture_title TEXT,                         -- Title of lecture, used for index pages and lecture page
  module_code   TEXT NOT NULL,                -- Module this lecture belongs to
  created_at    TEXT NOT NULL,                -- Date created (YYYY-MM-DD), used for filename
  slides_link   TEXT,                         -- Link to slides
  FOREIGN KEY (module_code) REFERENCES modules (module_id)
);

INSERT INTO modules (module_id, module_title, enrolled, year_of_study, semester, module_messages)
VALUES
  ('CS1106', 'Intro to Relational Databases', 1, 1, 1, 'rm -rf /var/opt/gitlab/postgresql/data/ - some GitLab database enginner in January 2017'),
  ('CS1111', 'Systems Organisation 1', 1, 1, 1, 'System Heirarchy uses abstraction to ignore the small details. It couldnt be too hard me to do it too, right? right?'),
  ('CS1115', 'Web Development 1', 1, 1, 1, 'HTML is for structure, CSS is for appearance - Derek Bridge'),
  ('CS1112', 'Foundations of Computer Science 1', 1, 1, 1, 'Some people think I''m bonkers, but I just think I''m free - Dizzee Rascal in Bonkers'),
  ('CS1117', 'Intro to Programming', 1, 1, 1, 'if python_easy(): pass_exams()'),
  ('MA1001', 'Calculus for Science 1', 1, 1, 1, 'Mathematics bullshit');