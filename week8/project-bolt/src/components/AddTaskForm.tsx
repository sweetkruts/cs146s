import { useState } from 'react';
import { Plus } from 'lucide-react';

type AddTaskFormProps = {
  onAdd: (title: string, description: string) => Promise<void>;
};

export function AddTaskForm({ onAdd }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    await onAdd(title, description);
    setTitle('');
    setDescription('');
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="What needs to be done?"
        className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
        disabled={loading}
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Add a description (optional)"
        className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
        rows={2}
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Plus size={20} />
        Add Task
      </button>
    </form>
  );
}
