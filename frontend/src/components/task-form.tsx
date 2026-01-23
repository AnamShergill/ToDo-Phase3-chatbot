'use client';

import React, { useState } from 'react';
import { useTask } from '@/context/task-context';
import { useAuth } from '@/context/auth-context';

interface TaskFormProps {
  task?: {
    id?: number;
    title: string;
    description?: string;
    priority?: string;
    due_date?: string;
  };
  onClose: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onClose }) => {
  const { createTask, updateTask } = useTask();
  const { user } = useAuth();

  const [formData, setFormData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    priority: task?.priority || 'medium',
    due_date: task?.due_date || ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate() || !user) return;

    setIsLoading(true);

    try {
      if (task && task.id) {
        // Update existing task
        await updateTask(user.id, task.id, formData);
      } else {
        // Create new task
        await createTask(user.id, formData);
      }

      onClose();
    } catch (err) {
      console.error('Error saving task:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="card w-full max-w-md bg-surface border-neon">
        <div className="p-6">
          <h2 className="text-xl font-bold mb-4 text-primary">
            {task?.id ? 'Edit Boom Task' : 'Create New Boom Task'}
          </h2>

          <form onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-muted mb-1">
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  className={`w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary ${
                    errors.title ? 'border-danger' : 'border-neon'
                  } input-field`}
                  placeholder="Task title"
                />
                {errors.title && (
                  <p className="mt-1 text-sm text-danger">{errors.title}</p>
                )}
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-muted mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
                  placeholder="Task description (optional)"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="priority" className="block text-sm font-medium text-muted mb-1">
                    Priority
                  </label>
                  <select
                    id="priority"
                    name="priority"
                    value={formData.priority}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="due_date" className="block text-sm font-medium text-muted mb-1">
                    Due Date
                  </label>
                  <input
                    type="date"
                    id="due_date"
                    name="due_date"
                    value={formData.due_date}
                    onChange={handleChange}
                    className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
                  />
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-sm font-medium text-muted border border-neon bg-surface hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary transition-all duration-200 shadow-neon-cyan"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="px-4 py-2 rounded-xl text-sm font-medium text-white bg-highlight-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary disabled:opacity-50 transition-all duration-200 transform hover:-translate-y-0.5 shadow-neon-purple"
              >
                {isLoading ? 'Saving...' : (task?.id ? 'Update Boom Task' : 'Create Boom Task')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TaskForm;