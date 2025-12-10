import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import './App.css';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [editingTask, setEditingTask] = useState(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/tasks/`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
      alert('Failed to load tasks');
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      await axios.post(`${API_URL}/tasks/`, taskData);
      loadTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      alert('Failed to create task');
    }
  };

  const handleUpdateTask = async (id, taskData) => {
    try {
      await axios.put(`${API_URL}/tasks/${id}/`, taskData);
      setEditingTask(null);
      loadTasks();
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (id) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/tasks/${id}/`);
      loadTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
      alert('Failed to delete task');
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header>
          <h1>Task Manager</h1>
          <p className="subtitle">Django + React Version</p>
        </header>

        <TaskForm
          editingTask={editingTask}
          onCreateTask={handleCreateTask}
          onUpdateTask={handleUpdateTask}
          onCancelEdit={handleCancelEdit}
        />

        <TaskList
          tasks={tasks}
          onEditTask={handleEditTask}
          onDeleteTask={handleDeleteTask}
        />
      </div>
    </div>
  );
}

export default App;

