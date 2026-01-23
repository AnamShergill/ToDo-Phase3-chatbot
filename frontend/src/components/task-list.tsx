'use client';

import React, { useState } from 'react';
import { useTask } from '@/context/task-context';
import TaskCard from './task-card';
import TaskForm from './task-form';

const TaskList: React.FC = () => {
  const { tasks, loading, error, fetchTasks } = useTask();
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);

  const handleEdit = (task: any) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCreate = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-highlight-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-danger/10 border-l-4 border-danger p-4 card glow-danger">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-danger" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-danger">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-primary">My Boom Tasks</h2>
        <button
          onClick={handleCreate}
          className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-medium text-white bg-highlight-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary transition-all duration-200 transform hover:-translate-y-0.5 shadow-neon-purple"
        >
          Create Boom Task
        </button>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-primary">No boom tasks yet</h3>
          <p className="mt-1 text-sm text-muted">Explode your productivity by creating your first task.</p>
          <div className="mt-6">
            <button
              onClick={handleCreate}
              className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-medium text-white bg-highlight-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary transition-all duration-200 transform hover:-translate-y-0.5 shadow-neon-purple"
            >
              Create Boom Task
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="mb-4 flex justify-between items-center">
            <p className="text-muted">{tasks.length} boom task{tasks.length !== 1 ? 's' : ''}</p>
          </div>
          <div className="space-y-3">
            {tasks.map(task => (
              <TaskCard key={task.id} task={task} onEdit={handleEdit} />
            ))}
          </div>
        </div>
      )}

      {showForm && (
        <TaskForm task={editingTask} onClose={handleCloseForm} />
      )}
    </div>
  );
};

export default TaskList;