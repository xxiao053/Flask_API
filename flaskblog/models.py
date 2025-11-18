sql_user = """
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        image_file TEXT NOT NULL DEFAULT 'default.jpg',
        password TEXT NOT NULL
    );
    """
sql_post = """
    CREATE TABLE IF NOT EXISTS post(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date_posted TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(id)
    );
    """
sql_insert_user = """
    INSERT INTO user (username, email, password)
    VALUES (:username, :email, :password)
"""
sql_task = """
    CREATE TABLE IF NOT EXISTS task(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed INTEGER DEFAULT 0
    );
"""
sql_payment = """
    CREATE TABLE IF NOT EXISTS payment(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL, -- avoid issue with float accuracy 
    currency TEXT NOT NULL, 
    status TEXT NOT NULL, -- created, pending, succeeded, failed, refunded, chargeback, chargeback_reversal 
    description TEXT, 
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
    );
"""
