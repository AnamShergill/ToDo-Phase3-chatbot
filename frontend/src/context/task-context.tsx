'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { taskApi } from '../lib/api';
import { useAuth } from './auth-context';

interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: string; // "low", "medium", "high"
  due_date?: string;
  created_at: string;
  updated_at: string;
}

interface TaskContextType {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: (userId: number, params?: {
    page?: number;
    limit?: number;
    status?: string;
    priority?: string;
    sort?: string;
  }) => Promise<void>;
  createTask: (userId: number, taskData: Partial<Task>) => Promise<void>;
  updateTask: (userId: number, taskId: number, taskData: Partial<Task>) => Promise<void>;
  updateTaskCompletion: (userId: number, taskId: number, completed: boolean) => Promise<void>;
  deleteTask: (userId: number, taskId: number) => Promise<void>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  const fetchTasks = async (userId: number, params?: {
    page?: number;
    limit?: number;
    status?: string;
    priority?: string;
    sort?: string;
  }) => {
    setLoading(true);
    setError(null);
    try {
      const response = await taskApi.getTasks(userId, params);
      setTasks(response.data.tasks);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (userId: number, taskData: Partial<Task>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await taskApi.createTask(userId, taskData);
      setTasks(prev => [...prev, response.data]);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (userId: number, taskId: number, taskData: Partial<Task>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await taskApi.updateTask(userId, taskId, taskData);
      setTasks(prev => prev.map(task => task.id === taskId ? response.data : task));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const updateTaskCompletion = async (userId: number, taskId: number, completed: boolean) => {
    setLoading(true);
    setError(null);
    try {
      const response = await taskApi.updateTaskCompletion(userId, taskId, completed);
      setTasks(prev => prev.map(task => task.id === taskId ? response.data : task));
    } catch (err: any) {
      setError(err.message || 'Failed to update task completion');
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (userId: number, taskId: number) => {
    setLoading(true);
    setError(null);
    try {
      await taskApi.deleteTask(userId, taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks for the current user when they log in
  useEffect(() => {
    if (user) {
      fetchTasks(user.id);
    } else {
      setTasks([]);
    }
  }, [user]);

  const value = {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    updateTaskCompletion,
    deleteTask,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};

export const useTask = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};