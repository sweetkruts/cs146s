import React, { useState, useEffect } from 'react';

function TaskForm({ editingTask, onCreateTask, onUpdateTask, onCancelEdit }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setDescription(editingTask.description || '');
      setCompleted(editingTask.completed);
    } else {
      setTitle('');
      setDescription('');
      setCompleted(false);
    }
  }, [editingTask]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const taskData = {
      title,
      description,
      completed
    };

    if (editingTask) {
      onUpdateTask(editingTask.id, taskData);
    } else {
      onCreateTask(taskData);
    }

    setTitle('');
    setDescription('');
    setCompleted(false);
  };

  return (
    <div className="task-form">
      <h2>{editingTask ? 'Edit Task' : 'Add New Task'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
            />
            <span>Completed</span>
          </label>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {editingTask ? 'Update Task' : 'Save Task'}
          </button>
          {editingTask && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onCancelEdit}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default TaskForm;

