from flask import request, jsonify, abort
from sqlalchemy import text
from flaskblog import app, engine 

# this is small service that allows client to manage the to-do list using URL + JSON 
# data is stored under SQLite 

# helper function
def task_row_to_dict(row):
    m = row._mapping  # dict-like, a SQLalchemy object
    # convert into a real python dict; jsonify requires real python dict 
    # return dict(row._mapping) also works 
    return {"id": m["id"],
            "title": m["title"],
            "description": m["description"],
            "completed": bool(m["completed"])}

# GET api/tasks (list)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT id, title, description, completed FROM task"
        ))
        # only read, no need transaction, so connect
        tasks = [task_row_to_dict(row) for row in result]
    return jsonify(tasks), 200 

# GET api/tasks/<id> (detail)
@app.route('/api/tasks/<int:task_id>', methods=["GET"])
def get_task(task_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, title, description, completed FROM task WHERE id = :id "),
                              {"id":task_id}).first()
        if result is None:
            # return jsonify({"status": "fail", "error":"Task not found"}), 404  # also work
            abort(404)
    return jsonify(task_row_to_dict(result)), 200 
    
# POST api/tasks (create)
@app.route('/api/tasks', methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        # simple validation
        return jsonify({"error": "title is required"}), 400 
    
    with engine.begin() as conn:
        # write record, so transaction is consitent and safe, so begin()
        result = conn.execute(
            text("""
                INSERT INTO task (title, description, completed)
                VALUES (:title, :description, 0)
                RETURNING id, title, description, completed
            """),
            {"title": title, "description": description}
            )
        row = result.first()
    return jsonify(task_row_to_dict(row)), 201

# PUT api/tasks/<id> (update)
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if data is None:
        return jsonify({"error": "No fields to update"}), 400
    
    with engine.begin() as conn:
        # check exists 
        exists = conn.execute(text("SELECT title, description, completed FROM task WHERE id = :id"), {"id": task_id}).first()
        if exists is None: 
            abort(404)

        # Allow partial update, otherwise use original values
        current = exists._mapping
        new_title = data.get("title", current["title"])
        new_description = data.get("description", current["description"])
        if "completed" in data: 
            # convert to 0/1 for SQLite
            new_completed = 1 if data["completed"] else 0
        else:
            new_completed = current["completed"]

        conn.execute(
            text(f"""
                UPDATE task
                SET title = :title, description = :description, completed = :completed
                WHERE id = :id
            """),
            {"id": task_id,
             "title": new_title,
             "description": new_description,
             "completed": new_completed}
            )
        
        result = conn.execute(
            text("SELECT id, title, description, completed FROM task WHERE id = :id"),
        {"id": task_id}
        ).first()

    return jsonify(task_row_to_dict(result)), 200 
    
# DELETE /api/tasks/<id> (delete)
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM task WHERE id = :id"),
            {"id": task_id}
        ).first()
        if not exists:
            abort(404)
        
        conn.execute(
            text("DELETE FROM task WHERE id = :id"),
            {"id": task_id}
        )
    
    return jsonify({"message": "Task deleted"}), 200 


            
        

