'use client';

import React, { useState } from 'react';
import { useTask } from '@/context/task-context';
import { useAuth } from '@/context/auth-context';

const TaskFilterBar: React.FC = () => {
  const { fetchTasks } = useTask();
  const { user } = useAuth();

  const [filters, setFilters] = useState({
    status: 'all',
    priority: '',
    sort: 'created',
  });

  const handleFilterChange = (filterType: string, value: string) => {
    const newFilters = { ...filters, [filterType]: value };
    setFilters(newFilters);

    if (user) {
      fetchTasks(user.id, {
        status: newFilters.status,
        priority: newFilters.priority || undefined,
        sort: newFilters.sort,
      });
    }
  };

  return (
    <div className="card p-4 mb-6 bg-surface border-neon">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label htmlFor="status" className="block text-sm font-medium text-muted mb-1">
            Status
          </label>
          <select
            id="status"
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
          >
            <option value="all">All Tasks</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
          </select>
        </div>

        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-muted mb-1">
            Priority
          </label>
          <select
            id="priority"
            value={filters.priority}
            onChange={(e) => handleFilterChange('priority', e.target.value)}
            className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label htmlFor="sort" className="block text-sm font-medium text-muted mb-1">
            Sort By
          </label>
          <select
            id="sort"
            value={filters.sort}
            onChange={(e) => handleFilterChange('sort', e.target.value)}
            className="w-full px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-highlight-primary input-field"
          >
            <option value="created">Created Date</option>
            <option value="due_date">Due Date</option>
            <option value="priority">Priority</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default TaskFilterBar;