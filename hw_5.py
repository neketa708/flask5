from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)
tasks = []

# Модель задачи
class Task:
    def __init__(self, title, description, status):
        self.id = uuid4()
        self.title = title
        self.description = description
        self.status = status

# Получение списка всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{"id": str(task.id), "title": task.title, "description": task.description, "status": task.status} for task in tasks])

# Получение задачи по ID
@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if str(task.id) == task_id:
            return jsonify({"id": str(task.id), "title": task.title, "description": task.description, "status": task.status})
    return jsonify({"message": "Task not found"}), 404

# Добавление новой задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], description=data['description'], status=data['status'])
    tasks.append(task)
    return jsonify({"id": str(task.id), "title": task.title, "description": task.description, "status": task.status}), 201

# Обновление задачи по ID
@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if str(task.id) == task_id:
            task.title = data['title']
            task.description = data['description']
            task.status = data['status']
            return jsonify({"id": str(task.id), "title": task.title, "description": task.description, "status": task.status})
    return jsonify({"message": "Task not found"}), 404

# Удаление задачи по ID
@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if str(task.id) == task_id:
            del tasks[i]
            return jsonify({"message": "Task deleted"})
    return jsonify({"message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)