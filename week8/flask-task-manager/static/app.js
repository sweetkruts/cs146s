const API_URL = 'http://localhost:5000/api';

let editingTaskId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    
    document.getElementById('taskForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('cancelBtn').addEventListener('click', resetForm);
});

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        
        const tasksList = document.getElementById('tasksList');
        
        if (tasks.length === 0) {
            tasksList.innerHTML = '<div class="empty-state"><p>No tasks yet. Create one to get started!</p></div>';
            return;
        }
        
        tasksList.innerHTML = tasks.map(task => `
            <div class="task-card ${task.completed ? 'completed' : ''}">
                <div class="task-header">
                    <h3 class="task-title">${escapeHtml(task.title)}</h3>
                    <span class="task-status ${task.completed ? 'completed' : 'pending'}">
                        ${task.completed ? 'Completed' : 'Pending'}
                    </span>
                </div>
                ${task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : ''}
                <div class="task-actions">
                    <button class="btn btn-edit" onclick="editTask(${task.id})">Edit</button>
                    <button class="btn btn-delete" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tasks:', error);
        alert('Failed to load tasks');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const completed = document.getElementById('completed').checked;
    
    const taskData = {
        title,
        description,
        completed
    };
    
    try {
        if (editingTaskId) {
            await fetch(`${API_URL}/tasks/${editingTaskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        } else {
            await fetch(`${API_URL}/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        }
        
        resetForm();
        loadTasks();
    } catch (error) {
        console.error('Error saving task:', error);
        alert('Failed to save task');
    }
}

async function editTask(id) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`);
        const task = await response.json();
        
        document.getElementById('taskId').value = task.id;
        document.getElementById('title').value = task.title;
        document.getElementById('description').value = task.description || '';
        document.getElementById('completed').checked = task.completed;
        
        document.getElementById('form-title').textContent = 'Edit Task';
        document.getElementById('cancelBtn').style.display = 'inline-block';
        
        editingTaskId = id;
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        console.error('Error loading task:', error);
        alert('Failed to load task');
    }
}

async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
    }
}

function resetForm() {
    document.getElementById('taskForm').reset();
    document.getElementById('taskId').value = '';
    document.getElementById('form-title').textContent = 'Add New Task';
    document.getElementById('cancelBtn').style.display = 'none';
    editingTaskId = null;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

