from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# --- Настройка базы данных ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Модель задачи ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "order": self.order
        }


# --- Маршруты ---
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.order).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    max_order = db.session.query(db.func.max(Task.order)).scalar() or 0
    new_task = Task(title=data['title'], order=max_order + 1)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    if 'done' in data:
        task.done = data['done']
    if 'title' in data:
        task.title = data['title']

    db.session.commit()
    return jsonify(task.to_dict())


@app.route('/reorder', methods=['POST'])
def reorder_tasks():
    data = request.get_json()
    order_list = data.get('order', [])
    for i, task_id in enumerate(order_list):
        task = Task.query.get(task_id)
        if task:
            task.order = i
    db.session.commit()
    return jsonify({'message': 'Order updated'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
