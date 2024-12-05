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
    );

INSERT INTO
    transactions (user_id, symbol, shares, price, date)
VALUES
    (1, "nflx", 5, 600.25, "2018-01-01 00:00:00");