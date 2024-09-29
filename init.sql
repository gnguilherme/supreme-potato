CREATE TABLE IF NOT EXISTS users (
    id INT SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS chats (
    id INT SERIAL PRIMARY KEY,
    user_id INT,
    chat_id TEXT,  -- This is a hash of the user_id, the chat_id, and the timestamp
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INT SERIAL PRIMARY KEY,
    chat_id INT,
    user_id TEXT,
    message TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);