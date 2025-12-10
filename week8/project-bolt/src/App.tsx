import { useEffect, useState } from 'react';
import { User } from '@supabase/supabase-js';
import { LogOut, ListTodo } from 'lucide-react';
import { supabase, Task } from './lib/supabase';
import { AuthForm } from './components/AuthForm';
import { AddTaskForm } from './components/AddTaskForm';
import { TaskItem } from './components/TaskItem';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      (async () => {
        setUser(session?.user ?? null);
        if (session?.user) {
          await fetchTasks();
        } else {
          setTasks([]);
        }
      })();
    });

    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    const { data, error } = await supabase
      .from('tasks')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching tasks:', error);
    } else {
      setTasks(data || []);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    if (!user) return;

    const { error } = await supabase.from('tasks').insert({
      user_id: user.id,
      title,
      description,
      completed: false,
    });

    if (error) {
      console.error('Error adding task:', error);
    } else {
      await fetchTasks();
    }
  };

  const handleUpdateTask = async (id: string, updates: Partial<Task>) => {
    const { error } = await supabase
      .from('tasks')
      .update({ ...updates, updated_at: new Date().toISOString() })
      .eq('id', id);

    if (error) {
      console.error('Error updating task:', error);
    } else {
      await fetchTasks();
    }
  };

  const handleDeleteTask = async (id: string) => {
    const { error } = await supabase.from('tasks').delete().eq('id', id);

    if (error) {
      console.error('Error deleting task:', error);
    } else {
      await fetchTasks();
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <AuthForm onAuthSuccess={() => {}} />;
  }

  const filteredTasks = tasks.filter((task) => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const activeCount = tasks.filter((t) => !t.completed).length;
  const completedCount = tasks.filter((t) => t.completed).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-3 rounded-xl">
              <ListTodo className="text-white" size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Task Manager</h1>
              <p className="text-sm text-gray-600">{user.email}</p>
            </div>
          </div>
          <button
            onClick={handleSignOut}
            className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-gray-50 text-gray-700 rounded-lg shadow-sm transition border border-gray-200"
          >
            <LogOut size={18} />
            Sign Out
          </button>
        </div>

        <div className="mb-6">
          <AddTaskForm onAdd={handleAddTask} />
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex gap-2">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  filter === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All ({tasks.length})
              </button>
              <button
                onClick={() => setFilter('active')}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  filter === 'active'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Active ({activeCount})
              </button>
              <button
                onClick={() => setFilter('completed')}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  filter === 'completed'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Completed ({completedCount})
              </button>
            </div>
          </div>

          <div className="p-4">
            {filteredTasks.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                {filter === 'all' && 'No tasks yet. Add one to get started!'}
                {filter === 'active' && 'No active tasks. Great job!'}
                {filter === 'completed' && 'No completed tasks yet.'}
              </div>
            ) : (
              <div className="space-y-3">
                {filteredTasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleUpdateTask}
                    onDelete={handleDeleteTask}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
