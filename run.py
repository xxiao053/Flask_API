from flaskblog import app, engine 
from flaskblog.models import sql_user, sql_post, sql_task, sql_payment
from sqlalchemy import text 

def create_table(query):
    with engine.begin() as conn:
        conn.execute(text(query))

if __name__ == "__main__":
    create_table(sql_user)
    create_table(sql_post)
    create_table(sql_task)
    create_table(sql_payment)
    app.run(debug=True)