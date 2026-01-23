'use client';

import React from 'react';
import { useTask } from '@/context/task-context';
import { useAuth } from '@/context/auth-context';
import { Trash2, Edit3 } from 'lucide-react';

interface TaskCardProps {
  task: {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    priority: string;
    due_date?: string;
    created_at: string;
    updated_at: string;
  };
  onEdit: (task: any) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit }) => {
  const { updateTaskCompletion, deleteTask } = useTask();
  const { user } = useAuth();

  const handleToggleCompletion = async () => {
    if (!user) return;
    await updateTaskCompletion(user.id, task.id, !task.completed);
  };

  const handleDelete = async () => {
    if (!user) return;
    if (window.confirm('Are you sure you want to delete this task?')) {
      await deleteTask(user.id, task.id);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-danger/20 text-danger';
      case 'medium': return 'bg-warning/20 text-warning';
      case 'low': return 'bg-success/20 text-success';
      default: return 'bg-muted/20 text-muted';
    }
  };

  return (
    <div className={`card p-4 mb-3 transition-all duration-200 ${
      task.completed
        ? 'opacity-75 border-success/30 glow-success'
        : 'hover:border-highlight-primary/50 hover:shadow-neon-purple-intense'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="mt-1 h-5 w-5 rounded border-border text-highlight-primary focus:ring-highlight-primary cursor-pointer bg-surface border-neon"
          />
          <div className="flex-1 min-w-0">
            <h3 className={`font-medium truncate ${
              task.completed ? 'line-through text-muted' : 'text-primary'
            }`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm truncate ${
                task.completed ? 'text-muted' : 'text-muted'
              }`}>
                {task.description}
              </p>
            )}
            <div className="mt-2 flex items-center space-x-3">
              {task.priority && (
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              )}
              {task.due_date && (
                <span className="text-xs text-muted">
                  Due: {formatDate(task.due_date)}
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="flex space-x-2 ml-2">
          <button
            onClick={() => onEdit(task)}
            className="p-1.5 rounded-md text-muted hover:bg-surface hover:text-primary transition-colors shadow-neon-cyan"
            aria-label="Edit task"
          >
            <Edit3 size={16} />
          </button>
          <button
            onClick={handleDelete}
            className="p-1.5 rounded-md text-muted hover:bg-danger/10 hover:text-danger transition-colors shadow-neon-red glow-danger"
            aria-label="Delete task"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;