# Finance app

WIP

## Initialize database

Add "finance.db" to /instance directory.

```
CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL,
        cash NUMERIC NOT NULL DEFAULT 10000.00
    );
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
```

## Start app

Run below to start app in development mode.

```
flask --app finance run --debug
```

## Inspiration

https://cs50.harvard.edu/x/2024/psets/9/finance/
