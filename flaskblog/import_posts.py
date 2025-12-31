import os  
import json 
from datetime import datetime, UTC
from sqlalchemy import create_engine, text

with open("./flaskblog/posts.json", "r", encoding="utf-8") as read_file:
    posts = json.load(read_file)  # List[dict]

for post in posts:
    if post['user_id'] == 1:
        post['user_id'] = 6
    else:
        post['user_id'] = 8

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_PATH = os.path.join(BASE_DIR, "blogsite.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
sql = """
    INSERT INTO post (title, date_posted, content, user_id)
    VALUES (:title, :date_posted, :content, :user_id)
"""
with engine.begin() as conn:
    for post in posts:
        conn.execute(text(sql), {"title": post['title'],
                                   "date_posted": datetime.now(UTC).replace(tzinfo=None),
                                    "content": post['content'],
                                    "user_id": post['user_id']})
