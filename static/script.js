async function loadTasks() {
    const res = await fetch('/tasks');
    const data = await res.json();
    const list = document.getElementById('taskList');
    list.innerHTML = '';
    data.forEach(task => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            ${task.title}
            <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const title = document.getElementById('taskTitle').value.trim();
    if (!title) return alert('Please enter a task title!');
    await fetch('/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title})
    });
    document.getElementById('taskTitle').value = '';
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/tasks/${id}`, {method: 'DELETE'});
    loadTasks();
}

window.onload = loadTasks;
