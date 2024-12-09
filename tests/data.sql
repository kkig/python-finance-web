INSERT INTO
    users (username, hash)
VALUES
    (
        "test",
        "pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f"
    ),
    (
        "other",
        "pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79"
    ),
    (
        "test2",
        "pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f"
    );

INSERT INTO
    transactions (user_id, symbol, shares, price, date)
VALUES
    (1, "NFLX", 5, 600.25, "2018-01-01 00:00:00"),
    (2, "NFLX", 3, 650.25, "2018-11-01 00:00:00"),
    (1, "NFLX", 1, 620.25, "2018-06-01 00:00:00"),
    (1, "AMZN", 5, 600.25, "2018-01-11 00:00:00");