from flaskblog import engine 
from flaskblog.models import sql_user, sql_post, sql_task, sql_payment
from sqlalchemy import text 

def create_table(query):
    with engine.begin() as conn:
        conn.execute(text(query))

if __name__ == "__main__":
    # the purpose of run.py is only to run app
    # so I move table creating tasks here
    # only run this script once to build db and tables
    create_table(sql_user)
    create_table(sql_post)
    create_table(sql_task)
    create_table(sql_payment)