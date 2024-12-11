# Finance app

Flask web application with SQLite to simulate stock trading (buying/selling) using real-time data from an external API.
Note: Currently implementing selling feature.

## Initialize database

Add "finance.db" to /instance directory.

```
CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        cash NUMERIC NOT NULL DEFAULT 10000.00
    );

CREATE TABLE
    transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price REAL NOT NULL,
        date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
```

## Start app

Run below to start app in development mode.

```
flask --app finance run --debug
```

## Inspiration

https://cs50.harvard.edu/x/2024/psets/9/finance/
