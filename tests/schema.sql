CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        cash NUMERIC NOT NULL DEFAULT 10000.00
    );

CREATE TABLE
    symbols (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        symbol TEXT NOT NULL UNIQUE
    );

CREATE TABLE
    transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        symbol_id INTEGER NOT NULL shares TEXT NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (symbol_id) REFERENCES symbols (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

-- CREATE TABLE sqlite_sequence(name,seq);
-- CREATE UNIQUE INDEX username ON users (username);