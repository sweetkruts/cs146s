import React from 'react';

function TaskList({ tasks, onEditTask, onDeleteTask }) {
  if (tasks.length === 0) {
    return (
      <div className="tasks-section">
        <h2>Tasks</h2>
        <div className="empty-state">
          <p>No tasks yet. Create one to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tasks-section">
      <h2>Tasks</h2>
      <div className="tasks-list">
        {tasks.map((task) => (
          <div
            key={task.id}
            className={`task-card ${task.completed ? 'completed' : ''}`}
          >
            <div className="task-header">
              <h3 className="task-title">{task.title}</h3>
              <span className={`task-status ${task.completed ? 'completed' : 'pending'}`}>
                {task.completed ? 'Completed' : 'Pending'}
              </span>
            </div>
            {task.description && (
              <p className="task-description">{task.description}</p>
            )}
            <div className="task-actions">
              <button
                className="btn btn-edit"
                onClick={() => onEditTask(task)}
              >
                Edit
              </button>
              <button
                className="btn btn-delete"
                onClick={() => onDeleteTask(task.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskList;

