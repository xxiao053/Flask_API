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
        date_posted DATETIME NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(id)
    );
    """
