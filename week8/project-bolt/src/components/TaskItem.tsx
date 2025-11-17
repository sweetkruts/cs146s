import { useState } from 'react';
import { CheckCircle2, Circle, Trash2, Edit2, X, Check } from 'lucide-react';
import { Task } from '../lib/supabase';

type TaskItemProps = {
  task: Task;
  onUpdate: (id: string, updates: Partial<Task>) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description);
  const [loading, setLoading] = useState(false);

  const handleToggleComplete = async () => {
    setLoading(true);
    await onUpdate(task.id, { completed: !task.completed });
    setLoading(false);
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) return;

    setLoading(true);
    await onUpdate(task.id, {
      title: editTitle,
      description: editDescription,
    });
    setIsEditing(false);
    setLoading(false);
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setLoading(true);
    await onDelete(task.id);
  };

  if (isEditing) {
    return (
      <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          placeholder="Task title"
          autoFocus
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
          placeholder="Description (optional)"
          rows={2}
        />
        <div className="flex gap-2">
          <button
            onClick={handleSaveEdit}
            disabled={loading || !editTitle.trim()}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition disabled:opacity-50"
          >
            <Check size={16} />
            Save
          </button>
          <button
            onClick={handleCancelEdit}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm font-medium transition"
          >
            <X size={16} />
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:shadow-md transition group">
      <div className="flex items-start gap-3">
        <button
          onClick={handleToggleComplete}
          disabled={loading}
          className="mt-0.5 flex-shrink-0 transition disabled:opacity-50"
        >
          {task.completed ? (
            <CheckCircle2 className="text-green-600" size={24} />
          ) : (
            <Circle className="text-gray-400 hover:text-gray-600" size={24} />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3
            className={`font-medium text-gray-800 mb-1 ${
              task.completed ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-600">{task.description}</p>
          )}
        </div>

        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="p-1.5 hover:bg-gray-100 rounded-lg transition"
            title="Edit task"
          >
            <Edit2 size={18} className="text-gray-600" />
          </button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="p-1.5 hover:bg-red-50 rounded-lg transition"
            title="Delete task"
          >
            <Trash2 size={18} className="text-red-600" />
          </button>
        </div>
      </div>
    </div>
  );
}
