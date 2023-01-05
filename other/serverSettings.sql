CREATE TABLE serverSettings(
  id INTEGER PRIMARY KEY,
  autoresponse INTEGER NOT NULL,
  autoresponse_content TEXT NOT NULL,
  blacklist TEXT NOT NULL
);