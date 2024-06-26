CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(36) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    initial_video TEXT NOT NULL,
    second_video TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);